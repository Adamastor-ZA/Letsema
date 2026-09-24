import { z } from 'zod'
import { datasetSchema, SCHEMA_VERSION, type Dataset } from '../schema/dataset'
import { DecryptError, decryptText, encryptText, isEncryptedEnvelope, type EncryptedEnvelope } from './crypto'

export const EXPORT_FORMAT = 'letsema-coverage'

const exportFileSchema = z.object({
  format: z.literal(EXPORT_FORMAT),
  schemaVersion: z.number().int(),
  exportedAt: z.string(),
  data: z.unknown(),
})

export function buildExport(dataset: Dataset, exportedAt: string): string {
  return JSON.stringify({ format: EXPORT_FORMAT, schemaVersion: SCHEMA_VERSION, exportedAt, data: dataset }, null, 2)
}

export async function buildEncryptedExport(dataset: Dataset, exportedAt: string, passphrase: string, iterations?: number): Promise<string> {
  return JSON.stringify(await encryptText(buildExport(dataset, exportedAt), passphrase, iterations), null, 2)
}

export function backupFilename(date: string, encrypted: boolean): string {
  return `coverage-backup-${date}${encrypted ? '.encrypted' : ''}.json`
}

export type ParsedBackup =
  | { kind: 'plain'; dataset: Dataset; exportedAt: string }
  | { kind: 'encrypted'; envelope: EncryptedEnvelope }

export class ImportError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'ImportError'
  }
}

function issueText(error: z.ZodError): string {
  const first = error.issues[0]
  if (!first) return 'The data is not valid.'
  const where = first.path.length ? ` at ${first.path.join('.')}` : ''
  return `${first.message}${where}${error.issues.length > 1 ? ` (and ${error.issues.length - 1} more)` : ''}.`
}

/** Recognise and validate a backup file. Throws ImportError with a reason the user can act on. */
export function parseBackup(text: string): ParsedBackup {
  let json: unknown
  try {
    json = JSON.parse(text)
  } catch {
    throw new ImportError('This is not a JSON file.')
  }
  if (isEncryptedEnvelope(json)) return { kind: 'encrypted', envelope: json }
  const file = exportFileSchema.safeParse(json)
  if (!file.success) throw new ImportError('This is not a Coverage backup.')
  if (file.data.schemaVersion > SCHEMA_VERSION) throw new ImportError('This backup was made by a newer version of the app.')
  if (file.data.schemaVersion !== SCHEMA_VERSION) throw new ImportError(`Unsupported backup version ${file.data.schemaVersion}.`)
  const dataset = datasetSchema.safeParse(file.data.data)
  if (!dataset.success) throw new ImportError(`The backup failed validation: ${issueText(dataset.error)}`)
  return { kind: 'plain', dataset: dataset.data as Dataset, exportedAt: file.data.exportedAt }
}

/** Decrypt an encrypted backup and validate what is inside. */
export async function openEncryptedBackup(envelope: EncryptedEnvelope, passphrase: string): Promise<Extract<ParsedBackup, { kind: 'plain' }>> {
  const text = await decryptText(envelope, passphrase)
  const inner = parseBackup(text)
  if (inner.kind !== 'plain') throw new DecryptError('The file is damaged.')
  return inner
}
