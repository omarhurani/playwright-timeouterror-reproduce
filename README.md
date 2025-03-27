# Playwright Bug Reproduction - `TimeoutError` is never received

This project is a minimal example to reproduce a bug in Playwright where the `TimeoutError` is never received when a navigation fails. The error shows up in the trace, and is reported as `Future exception was never retrieved` if the app completes normally.

## Summary

I am only able to reproduce this issue when deploying the app to Fly.io, so a Fly.io account is required to reproduce this issue with the steps I provided.

To reproduce the issue, tracing must be enabled with both screenshots and snapshots.

This issue does not happen often, but it happens on select websites semi-consistently. The example I provided requires setting a user agent to avoid the website blocking the request.

Website: `https://www.flychicago.com/business/opportunities/bidscontracts/alerts/Pages/article.aspx?newsid=1666`
User agent: `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36`


## Steps to reproduce

1. Clone this repository
2. Make sure to have [flyctl](https://fly.io/docs/flyctl/install/) installed and logged in. 
3. Launch the app on Fly.io `fly launch --name <app-name>`
   - To redeploy, use `fly deploy`
4. After the app is deployed, send a request to it with the faulty website. 
   - If the response error is `"Asyncio timeout"`, the issue has been reproduced.
   - It might require multiple requests to reproduce the issue.
```
curl --location 'https://<app-name>.fly.dev/api/go-to-url?url=https%3A%2F%2Fwww.flychicago.com%2Fbusiness%2Fopportunities%2Fbidscontracts%2Falerts%2FPages%2Farticle.aspx%3Fnewsid%3D1666&ua=Mozilla%2F5.0%20(X11%3B%20Linux%20x86_64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F134.0.0.0%20Safari%2F537.36&trace=true'
```

5. (Optional) Fetch the trace. The trace will be deleted if the app is shutdown or redeployed, so make sure to fetch the trace quickly after reproducing the issue. 
```
curl --location 'https://<app-name>.fly.dev/api/get-trace' > trace.zip
```

