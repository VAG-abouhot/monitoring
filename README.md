<p align="center">
    <h4 align="center">The readme/code you are seeing it's part of upcoming first release</h4>
    <h2 align="center">Valid&GO API Client Python v1</h2>
</p>

**[Valid&GO Monitoring](https://www.monitoring.validandgo.com)** is a hosted monitoring engine capable of delivering visibility into machine learning algorithms deployed in production.

This readme/code introduces the first Valid&GO API Client Python v1. 

**Development Status**: Alpha.

First, install Valid&GO Monitoring - API Client Python v1:
```
pip install git+https://github.com/VAG-abouhot/monitoring
```

### Quick start example:

```py

from monitoring.client import Client

client = Client.connect(
    "VALIDANDGO_API_ID", 
    "VALIDANDGO_API_KEY"
)


session = client.monitoring_session('my_application_name', 'my_model_name')

session.start()
session.set_data(data_model_input, data_model_output, metadata)
# Your deployed model code
session.stop()


```