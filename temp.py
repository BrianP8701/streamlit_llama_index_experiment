import toml

output_file = ".streamlit/secrets.toml"
with open("/Users/brianprzezdziecki/Code/onno/secrets/onno-404216-firebase-adminsdk-3ejg7-6ea6cb91cc.json") as json_file:
    json_text = json_file.read()
config = {"textkey": json_text}
toml_config = toml.dumps(config)
with open(output_file, "w") as target:
    target.write(toml_config)