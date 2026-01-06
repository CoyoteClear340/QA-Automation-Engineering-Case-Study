## Root Cause

| **Issues**            | **Locally**                               | **CI/CD**                                                                 |
|----------------------|-------------------------------------------|---------------------------------------------------------------------------|
| No wait after Login  | Fast CPU                                  | Slow VM, delays                                                           |
| Strict URL           | Simple redirect, no params                | Extra query params                                                        |
| Random 2FA           | Trusted devices (No 2FA)                  | New VM IP may need 2FA (or some users have 2FA enabled by default)       |
| Case-sensitive test  | Same data always                          | Different fixtures, capitalization                                       |
| API timing           | Stable backend locally                    | Delayed responses, retries                                               |
