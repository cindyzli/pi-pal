export const dynamic = 'force-static'
import { MongoClient } from 'mongodb'

export async function GET() {
    const client = await MongoClient.connect(process.env.MONGODB_URI);
    const database = client.db('pi-pal')
    const collection = database.collection('stats')
    const patients = await collection.find().toArray()
    await client.close()
    return new Response(JSON.stringify(patients.reverse()), {
        headers: {
            'content-type': 'application/json',
        },
    })
}



// import { MongoClient } from 'mongodb'
// // export const dynamic = 'force-static'

// export async function queryLlamaIndex(query) {
//     const index = await getIndex();
//     const response = await index.query(query);
//     return response;
// }

// async function getIndex() {
//     const client = await MongoClient.connect(process.env.MONGODB_URI);
//     const database = client.db('pi-pal');
//     const collection = database.collection('stats');
//     const patients = await collection.find().toArray();
//     const documents = patients.map(patient => {
//         return new Document({
//             text: JSON.stringify(patient),
//             metadata: patient
//         });
//     });
//     const index = VectorStoreIndex.from_documents(documents);
//     await client.close();
//     return index;
// }

// export async function chatWithGPT(query) {
//     const openai = new OpenAIApi(new Configuration({
//         apiKey: process.env.OPENAI_API_KEY,
//     }));

//     const indexedData = await queryLlamaIndex(query);

//     const prompt = `Answer the following based on the given data: ${indexedData}`;

//     try {
//         const gptResponse = await openai.createCompletion({
//             model: 'text-davinci-003',
//             prompt: prompt,
//             max_tokens: 150,
//         });

//         return gptResponse.data.choices[0].text.trim();
//     } catch (error) {
//         console.error("Error querying GPT:", error);
//         return "Sorry, I couldn't process your request.";
//     }
// }

// export async function GET() {
//     const query = "Any patterns you see in the patient history";
//     const response = await chatWithGPT(query);

//     return new Response(JSON.stringify({ message: response }), {
//         headers: {
//             'content-type': 'application/json',
//         },
//     });
// }