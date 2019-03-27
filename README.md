# monitoring


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