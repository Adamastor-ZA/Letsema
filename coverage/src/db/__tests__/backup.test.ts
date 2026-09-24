import { describe, expect, it } from 'vitest'
import { buildSampleInputs } from '../../sample/sample-data'
import { defaultSettings } from '../../schema/settings'
import { inputsToDataset } from '../../schema/dataset'
import { backupFilename, buildEncryptedExport, buildExport, ImportError, openEncryptedBackup, parseBackup } from '../backup'
import { DecryptError, decryptText, encryptText, isEncryptedEnvelope, KDF_ITERATIONS } from '../crypto'

const dataset = inputsToDataset(buildSampleInputs('2026-09'), defaultSettings('2026-09'))
const FAST = 1_000 // keep tests quick; production uses KDF_ITERATIONS
const pass = 'correct horse battery staple'

describe('plain backups', () => {
  it('round-trips the whole dataset', () => {
    const parsed = parseBackup(buildExport(dataset, '2026-09-24T10:00:00.000Z'))
    expect(parsed).toEqual({ kind: 'plain', dataset, exportedAt: '2026-09-24T10:00:00.000Z' })
  })

  it('rejects files that are not valid backups, with a reason', () => {
    expect(() => parseBackup('not json')).toThrow(new ImportError('This is not a JSON file.'))
    expect(() => parseBackup('{"hello":1}')).toThrow('This is not a Coverage backup.')
    const file = JSON.parse(buildExport(dataset, 'x'))
    expect(() => parseBackup(JSON.stringify({ ...file, schemaVersion: 99 }))).toThrow('newer version')
    const broken = { ...file, data: { ...file.data, assets: [{ ...file.data.assets[0], valueCents: -5 }] } }
    expect(() => parseBackup(JSON.stringify(broken))).toThrow(/failed validation: Cannot be negative at assets\.0\.valueCents/)
  })

  it('names files by date', () => {
    expect(backupFilename('2026-09-24', false)).toBe('coverage-backup-2026-09-24.json')
    expect(backupFilename('2026-09-24', true)).toBe('coverage-backup-2026-09-24.encrypted.json')
  })
})

describe('encryption', () => {
  it('uses the recommended work factor by default', async () => {
    expect(KDF_ITERATIONS).toBeGreaterThanOrEqual(600_000)
    const envelope = await encryptText('x', pass)
    expect(envelope.kdf.iterations).toBe(KDF_ITERATIONS)
  })

  it('round-trips text, including non-ASCII', async () => {
    const text = 'Rand R 12 000 · café · 日本'
    const envelope = await encryptText(text, pass, FAST)
    expect(isEncryptedEnvelope(envelope)).toBe(true)
    expect(envelope.ciphertext).not.toContain('Rand')
    expect(await decryptText(envelope, pass)).toBe(text)
  })

  it('uses a fresh salt and IV every time', async () => {
    const [a, b] = await Promise.all([encryptText('same', pass, FAST), encryptText('same', pass, FAST)])
    expect(a.kdf.salt).not.toBe(b.kdf.salt)
    expect(a.cipher.iv).not.toBe(b.cipher.iv)
    expect(a.ciphertext).not.toBe(b.ciphertext)
  })

  it('fails cleanly on a wrong passphrase or a tampered file', async () => {
    const envelope = await encryptText('secret', pass, FAST)
    await expect(decryptText(envelope, 'wrong passphrase!!')).rejects.toBeInstanceOf(DecryptError)
    const bytes = atob(envelope.ciphertext)
    const flipped = String.fromCharCode(bytes.charCodeAt(0) ^ 1) + bytes.slice(1)
    await expect(decryptText({ ...envelope, ciphertext: btoa(flipped) }, pass)).rejects.toBeInstanceOf(DecryptError)
    await expect(decryptText({ ...envelope, cipher: { ...envelope.cipher, iv: 'AAAA' } }, pass)).rejects.toThrow('damaged')
    await expect(decryptText({ ...envelope, kdf: { ...envelope.kdf, iterations: 1e9 } }, pass)).rejects.toThrow('unsupported')
  })

  it('rejects short passphrases', async () => {
    await expect(encryptText('x', 'short')).rejects.toThrow(/at least 12/)
  })

  it('round-trips a full encrypted backup', async () => {
    const text = await buildEncryptedExport(dataset, '2026-09-24T10:00:00.000Z', pass, FAST)
    expect(text).not.toContain('sample')
    const parsed = parseBackup(text)
    expect(parsed.kind).toBe('encrypted')
    if (parsed.kind !== 'encrypted') return
    expect((await openEncryptedBackup(parsed.envelope, pass)).dataset).toEqual(dataset)
    await expect(openEncryptedBackup(parsed.envelope, 'not the passphrase')).rejects.toBeInstanceOf(DecryptError)
  })
})
