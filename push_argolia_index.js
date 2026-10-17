/*
上传 algolia 索引文件
参考：https://www.algolia.com/doc/guides/getting-started/quick-start/tutorials/quick-start-with-the-api-client/javascript/?client=javascript
*/

// For the default version
const algoliasearch = require("algoliasearch")

const appID = "747LJ10EI7"
const indexName = "ryan-space"
const indexFile = "./public/index.json"

function normalizeRecords(records) {
  const seen = new Set()
  return records.map((record) => {
    if (!record.uri) {
      throw new Error(`search record ${record.objectID || "?"} has no uri`)
    }
    if (seen.has(record.uri)) {
      throw new Error(`duplicate uri in search index: ${record.uri}`)
    }
    seen.add(record.uri)
    // The theme reuses objectIDs for sibling headings; uri is unique per record.
    return { ...record, objectID: record.uri }
  })
}

async function main() {
  const adminKey = process.env.ALGOLIA_ADMIN_KEY
  if (!adminKey) {
    throw new Error("ALGOLIA_ADMIN_KEY is not set")
  }

  const records = normalizeRecords(require(indexFile))
  const client = algoliasearch(appID, adminKey)
  const index = client.initIndex(indexName)

  const before = await index.search("", { hitsPerPage: 0 })
  console.log(`Before: ${before.nbHits} records`)

  await index.replaceAllObjects(records, { safe: true })

  const after = await index.search("", { hitsPerPage: 0 })
  console.log(`After: ${after.nbHits} records (expected ${records.length})`)
  if (after.nbHits !== records.length) {
    throw new Error(`Algolia record count mismatch: ${after.nbHits} != ${records.length}`)
  }
}

if (require.main === module) {
  main().catch((error) => {
    console.error(error)
    process.exitCode = 1
  })
}

module.exports = { normalizeRecords }
