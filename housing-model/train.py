import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

mlflow.set_tracking_uri("http://localhost:5000")

def main():
    print("Début du script d'entraînement")

    # 1. Charger le dataset
    df = pd.read_csv("california_housing.csv")
    print("Dimensions du dataset :", df.shape)

    # 2. Supprimer la colonne 'ocean_proximity'
    if "ocean_proximity" in df.columns:
        df = df.drop("ocean_proximity", axis=1)
        print("La colonne 'ocean_proximity' a été supprimée.")

    # 3. Séparer X (features) et y (cible)
    X = df.drop("median_house_value", axis=1)
    y = df["median_house_value"]

    # 4. Construire un pipeline simple : imputation + régression linéaire
    pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="mean")),
        ("regressor", LinearRegression())
    ])

    print("Avant pipeline.fit")
    pipeline.fit(X, y)
    print("Après pipeline.fit")

    # 5. Calcul de la métrique (ex. R²)
    r2_score = pipeline.score(X, y)

    # 6. Loguer le run avec MLflow
    with mlflow.start_run() as run:
        mlflow.log_metric("r2_score", r2_score)
        mlflow.log_param("model_type", "Pipeline_LinearRegression_without_ocean_proximity")
        
        # Fournir un exemple d'entrée pour la signature du modèle
        input_example = X.iloc[:5]
        
        mlflow.sklearn.log_model(
            sk_model=pipeline,
            artifact_path="model",
            input_example=input_example
        )

        print("Run ID :", run.info.run_id)
        print(f"Modèle entraîné, R² = {r2_score:.3f}")

    print("Fin du script d'entraînement")

if __name__ == "__main__":
    main()