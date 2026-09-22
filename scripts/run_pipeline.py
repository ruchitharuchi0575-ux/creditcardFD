import sys
import subprocess

# Force UTF-8 encoding on standard output for Windows terminal compatibility
sys.stdout.reconfigure(encoding='utf-8')

def run_step(step_name, command):
    print(f"\n[INFO] Executing Step: {step_name}...")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"[ERROR] Error in {step_name}. Pipeline halted.")
        sys.exit(1)
    print(f"[SUCCESS] {step_name} completed successfully!")

if __name__ == "__main__":
    print("STARTING END-TO-END TIER 4 DATA & ML PIPELINE")
    
    run_step("Data Cleaning", "python scripts/data_cleaning.py")
    run_step("Data Quality Validation", "python scripts/validate_data.py")
    run_step("Feature Engineering", "python scripts/feature_engineering.py")
    run_step("Model Training", "python scripts/train_model.py")
    run_step("Batch Prediction", "python scripts/predict_batch.py")
    
    print("\n[SUCCESS] PIPELINE EXECUTED SUCCESSFULLY!")