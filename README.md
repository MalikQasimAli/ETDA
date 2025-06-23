
# Eye-tracking data analysis (ET-DA) framework

An open-source library to extract events and measurements from raw eye-tracking data. 






## Deployment

To deploy this project download or pull

```bash
  https://github.com/MalikQasimAli/ETDA.git
```


## How to work with ET-DA

1. Fill up required values in JSON file in the ET-DA library:

```bash
  data -> etz_json.json
```

2. Create a new .py file in the etz directory.

3. Initilize the library: 
```bash
  etz = EtzLib()
```
4. Validate csv and JSON
```bash
 pd= etz.validate_csv_columns('/path/name.csv','et')
```
5. check all available functions and documentation by just writing 
```bash
 etz.
```
as shown in following figure.
