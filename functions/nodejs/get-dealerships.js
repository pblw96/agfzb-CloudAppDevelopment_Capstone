const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator
  });
  cloudant.setServiceUrl(params.COUCH_URL);

  try {
    let dealers = await cloudant.postAllDocs({
      db: 'dealerships',
      includeDocs: true,
    });

    let finalResult = dealers.result.rows.map(row => {
      const { _id, _rev, full_name, short_name, ...payload } = row.doc;
      return payload;
    });

    if (params.state) {
      finalResult = finalResult.filter(elem => {
        return elem.state === params.state;
      });
    }

    return ({
      headers: { 'Content-Type': 'application/json' },
      statusCode: 200,
      body: finalResult,
    });
  }
  catch (error) {
    return { error: error.description };
  }
}