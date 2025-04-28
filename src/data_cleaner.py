import pandas as pd

def extract_ref_fab(text: str) -> str | None:
    """Extracts the Ref./Fab value from the product text block."""
    for line in text.splitlines():
        if line.strip().startswith("Ref./Fab:"):
            parts = line.split(":", 1) # Split only on the first colon
            if len(parts) > 1:
                return parts[1].strip() # Get the part after the colon and strip whitespace
    return None # Return None if the line is not found

def main():
    products = pd.read_csv("products.csv")
    
    # replace sku column with ref/fab column
    products["sku"] = products["sku"].apply(extract_ref_fab)
    
    # save to csv
    products.to_csv("products_cleaned.csv", index=False)
    
if __name__ == "__main__":
    main()
