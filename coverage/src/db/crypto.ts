/**
 * Passphrase encryption for backups, using only the browser's WebCrypto:
 * AES-GCM (256-bit key, 96-bit random IV) with the key derived by
 * PBKDF2-SHA-256 over a 128-bit random salt. GCM authenticates the
 * ciphertext, so a wrong passphrase or a tampered file fails to decrypt
 * rather than producing garbage.
 */

export const ENCRYPTED_FORMAT = 'letsema-coverage-encrypted'
/** OWASP's 2023 recommendation for PBKDF2-HMAC-SHA256. */
export const KDF_ITERATIONS = 600_000
export const MIN_PASSPHRASE_LENGTH = 12
const MAX_ITERATIONS = 10_000_000

export interface EncryptedEnvelope {
  format: typeof ENCRYPTED_FORMAT
  version: 1
  kdf: { name: 'PBKDF2'; hash: 'SHA-256'; iterations: number; salt: string }
  cipher: { name: 'AES-GCM'; iv: string }
  ciphertext: string
}

export class DecryptError extends Error {
  constructor(message = 'Could not decrypt: the passphrase is wrong or the file is damaged.') {
    super(message)
    this.name = 'DecryptError'
  }
}

function toBase64(bytes: Uint8Array): string {
  let binary = ''
  const chunk = 0x8000
  for (let i = 0; i < bytes.length; i += chunk) binary += String.fromCharCode(...bytes.subarray(i, i + chunk))
  return btoa(binary)
}

function fromBase64(text: string): Uint8Array<ArrayBuffer> {
  const binary = atob(text)
  const bytes = new Uint8Array(binary.length)
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i)
  return bytes
}

/** The envelope's fixed header is bound to the ciphertext as additional authenticated data. */
function aad(): Uint8Array<ArrayBuffer> {
  return new TextEncoder().encode(`${ENCRYPTED_FORMAT}/1`)
}

async function deriveKey(passphrase: string, salt: Uint8Array<ArrayBuffer>, iterations: number): Promise<CryptoKey> {
  const material = await crypto.subtle.importKey('raw', new TextEncoder().encode(passphrase.normalize('NFC')), 'PBKDF2', false, ['deriveKey'])
  return crypto.subtle.deriveKey({ name: 'PBKDF2', hash: 'SHA-256', salt, iterations }, material, { name: 'AES-GCM', length: 256 }, false, [
    'encrypt',
    'decrypt',
  ])
}

export async function encryptText(plaintext: string, passphrase: string, iterations = KDF_ITERATIONS): Promise<EncryptedEnvelope> {
  if (passphrase.length < MIN_PASSPHRASE_LENGTH) throw new Error(`Use a passphrase of at least ${MIN_PASSPHRASE_LENGTH} characters`)
  const salt = crypto.getRandomValues(new Uint8Array(16))
  const iv = crypto.getRandomValues(new Uint8Array(12))
  const key = await deriveKey(passphrase, salt, iterations)
  const ciphertext = await crypto.subtle.encrypt({ name: 'AES-GCM', iv, additionalData: aad() }, key, new TextEncoder().encode(plaintext))
  return {
    format: ENCRYPTED_FORMAT,
    version: 1,
    kdf: { name: 'PBKDF2', hash: 'SHA-256', iterations, salt: toBase64(salt) },
    cipher: { name: 'AES-GCM', iv: toBase64(iv) },
    ciphertext: toBase64(new Uint8Array(ciphertext)),
  }
}

export function isEncryptedEnvelope(value: unknown): value is EncryptedEnvelope {
  if (typeof value !== 'object' || value === null) return false
  const v = value as Partial<EncryptedEnvelope>
  return (
    v.format === ENCRYPTED_FORMAT &&
    v.version === 1 &&
    v.kdf?.name === 'PBKDF2' &&
    v.kdf.hash === 'SHA-256' &&
    Number.isInteger(v.kdf.iterations) &&
    typeof v.kdf.salt === 'string' &&
    v.cipher?.name === 'AES-GCM' &&
    typeof v.cipher.iv === 'string' &&
    typeof v.ciphertext === 'string'
  )
}

export async function decryptText(envelope: EncryptedEnvelope, passphrase: string): Promise<string> {
  const { iterations } = envelope.kdf
  if (iterations < 1 || iterations > MAX_ITERATIONS) throw new DecryptError('This file uses unsupported encryption settings.')
  let salt: Uint8Array<ArrayBuffer>, iv: Uint8Array<ArrayBuffer>, data: Uint8Array<ArrayBuffer>
  try {
    salt = fromBase64(envelope.kdf.salt)
    iv = fromBase64(envelope.cipher.iv)
    data = fromBase64(envelope.ciphertext)
  } catch {
    throw new DecryptError('The file is damaged.')
  }
  if (iv.length !== 12 || salt.length < 16) throw new DecryptError('The file is damaged.')
  const key = await deriveKey(passphrase, salt, iterations)
  try {
    const plain = await crypto.subtle.decrypt({ name: 'AES-GCM', iv, additionalData: aad() }, key, data)
    return new TextDecoder().decode(plain)
  } catch {
    throw new DecryptError()
  }
}
