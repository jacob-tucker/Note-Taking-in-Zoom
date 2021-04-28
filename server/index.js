'use strict';

const fs = require('fs');
const path = require('path');
const http = require('http');
const url = require('url');
const opn = require('open');
const destroyer = require('server-destroy');

const { google } = require('googleapis');

/**
 * To use OAuth2 authentication, we need access to a a CLIENT_ID, CLIENT_SECRET, 
 * AND REDIRECT_URI.  To get these credentials for your application, visit 
 * https://console.cloud.google.com/apis/credentials.
 */
const keyPath = path.join(__dirname, 'oauth2.keys.json');
let keys = { redirect_uris: [''] };
if (fs.existsSync(keyPath)) {
    keys = require(keyPath).web;
}

/**
 * Create a new OAuth2 client with the configured keys.
 */
const oauth2Client = new google.auth.OAuth2(
    keys.client_id,
    keys.client_secret,
    keys.redirect_uris[0]
);

/**
 * This is one of the many ways you can configure googleapis to use 
 * authentication credentials.  In this method, we're setting a global reference for 
 * all APIs.  Any other API you use here, like google.drive('v3'), will now use this 
 * auth client. You can also override the auth client at the service and method call levels.
 */
google.options({ auth: oauth2Client });

/**
 * Open an http server to accept the oauth callback. In this simple example, 
 * the only request to our webserver is to /callback?code=<code>
 */
async function authenticate(scopes) {
    return new Promise((resolve, reject) => {
        // grab the url that will be used for authorization
        const authorizeUrl = oauth2Client.generateAuthUrl({
            access_type: 'offline',
            scope: scopes.join(' '),
        });
        const server = http
            .createServer(async (req, res) => {
                try {
                    if (req.url.indexOf('/oauth2callback') > -1) {
                        const qs = new url.URL(req.url, 'http://localhost:3000')
                            .searchParams;
                        res.end('Authentication successful! Please return to the console.');
                        server.destroy();
                        const { tokens } = await oauth2Client.getToken(qs.get('code'));
                        oauth2Client.credentials = tokens; // eslint-disable-line require-atomic-updates
                        resolve(oauth2Client);
                    }
                } catch (e) {
                    reject(e);
                }
            })
            .listen(3000, () => {
                // open the browser to the authorize url to start the workflow
                opn(authorizeUrl, { wait: false }).then(cp => cp.unref());
            });
        destroyer(server);
    });
}

async function runSample() {
    // retrieve user profile
    const service = google.drive('v3');
    const res = await service.files.list({
        pageSize: 10,
        fields: 'nextPageToken, files(id, name)',
    });
    const files = res.data.files;
    if (files.length === 0) {
        console.log('No files found.');
    } else {
        console.log('Files:');
        for (const file of files) {
            console.log(`${file.name} (${file.id})`);
        }
    }
}

/**
 * Retrieve a list of revisions.
 *
 * @param {String} fileId ID of the file to retrieve revisions for.
 * @param {Function} callback Function to call when the request is complete.
 */
async function retrieveRevisions(fileId) {
    // retrieve user profile
    const service = google.drive('v3');
    const res = await service.revisions.list({
        'fileId': fileId
    });
    console.log(res.data)
}

/**
 * Print information about the specified revision.
 *
 * @param {String} fileId ID of the file to print revision for.
 * @param {String} revisionId ID of the revision to print.
 */
async function printRevisionTime(fileId, revisionId) {
    // retrieve user profile
    const service = google.drive('v3');
    var res = await service.revisions.get({
        'fileId': fileId,
        'revisionId': revisionId
    });
    console.log(res.data.modifiedTime)
}

const scopes = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
];

authenticate(scopes)
    //.then(client => runSample())
    //.then(client => retrieveRevisions("195J8C_-uQN0L5WsrlloDG33zf8VupbQUxQlf8pWjKl4"))
    .then(client => printRevisionTime("195J8C_-uQN0L5WsrlloDG33zf8VupbQUxQlf8pWjKl4", 1))
    .catch(console.error);