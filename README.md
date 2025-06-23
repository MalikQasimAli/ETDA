
# Eye-tracking data analysis (ET-DA) framework

An open-source library to extract events and measurements from raw eye-tracking data. 

<img src="https://github.com/user-attachments/assets/a304afc1-37cd-40c6-9d52-ab4426a71f30" alt="allgroups_circular_pyschopy" width="300"/>




## Deployment

To deploy this project, download or pull

```bash
  https://github.com/MalikQasimAli/ETDA.git
```


## How to work with ET-DA

1. Fill in the required values in the JSON file in the ET-DA library:

```bash
  data -> etz_json.json
```

2. Create a new .py file in the etz directory.

3. Initialize the library: 
```bash
  etz = EtzLib()
```
4. Validate CSV and JSON
```bash
 pd= etz.validate_csv_columns('/path/name.csv','et')
```
5. Check all available functions and documentation by just writing 
```bash
 etz.
```
As shown in the following figure.
<div align="center">
  <img src="https://github.com/user-attachments/assets/fcd66c1c-8a04-4b33-9dcc-d4f7f21b510a" alt="etz" width="400"/>
</div>

<div align="center">
  <img src="https://github.com/user-attachments/assets/46a1d293-2ffd-45f2-96b6-96912978bd5a" alt="etz2" width="400"/>
</div>



