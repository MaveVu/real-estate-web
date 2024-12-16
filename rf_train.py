import pandas as pd
from sklearn.preprocessing import StandardScaler, Normalizer, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor


def train_rf_model():
    # reading the data
    all_properties = pd.read_csv("../data/curated/houses_all_properties.csv")

    # stratifying using SA2_Name (suburb's name) and filtering out suburbs with < 50 props
    stratify_column = 'SA2_Name'
    house_counts = all_properties[stratify_column].value_counts()
    all_properties = all_properties[all_properties[stratify_column].isin(house_counts[house_counts >= 50].index)]

    # converting categorical attributes to numerical
    mapping = {category: index for index, category in enumerate(all_properties['SA2_Name'].unique())}
    all_properties['map_SA2_Name'] = all_properties['SA2_Name'].map(mapping)
    all_properties['type'] = all_properties['type'].apply(lambda x: 0 if x == 'House' else 1) 

    # filtering for needed columns
    columns = ['SA2_Name', 'parking', 'type', 'num_schools', 'cost', 'beds', 'baths',
                'closest_train_station_distance_km', 'closest_tram_station_distance_km', 'closest_hospital_distance_km',
                'closest_grocery_distance_km', 'Net_migration_2021_22', 'Net_migration_2022_23', 'ERP_per_km2_2021',
                'ERP_per_km2_2022', 'ERP_per_km2_2023', 'ERP_increase_2020_21', 'ERP_increase_2021_22', 'ERP_increase_2022_23',
                'NUMBER_OF_JOBS_PERSONS_2020-21', 'MEDIAN_INCOME_PERSONS_2020-21', 'map_SA2_Name']
    all_properties = all_properties[columns]

    # normalizing the data
    exclude_columns = ['parking', 'type', 'num_schools', 'beds', 'baths', 'map_SA2_Name', 'cost']
    columns_to_scale = [col for col in all_properties.columns if all_properties[col].dtype != object and col not in exclude_columns]
    scaler = MinMaxScaler()
    data_scaled = all_properties.copy()
    data_scaled[columns_to_scale] = scaler.fit_transform(data_scaled[columns_to_scale])

    # splitting train-test (80-20)
    X = data_scaled.drop(columns=["cost", "SA2_Name"])
    y = data_scaled["cost"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=data_scaled['map_SA2_Name']
    )

    # random forest regression
    rf_model = RandomForestRegressor(max_depth = 5)
    rf_model.fit(X_train, y_train)
    return rf_model
