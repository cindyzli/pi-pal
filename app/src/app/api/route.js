export const dynamic = 'force-static'
import {MongoClient} from 'mongodb'
 
export async function GET() {
    const client = await MongoClient.connect(process.env.MONGODB_URI);
    const database = client.db('pi-pal')
    const collection = database.collection('stats')
    const patients = await collection.find().toArray()
    await client.close()
    return new Response(JSON.stringify(patients), {
        headers: {
            'content-type': 'application/json',
        },
    })
}