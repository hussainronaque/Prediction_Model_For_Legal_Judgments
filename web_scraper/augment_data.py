import pandas as pd
from textattack.augmentation import WordNetAugmenter

# Create the WordNet augmenter from TextAttack
augmenter = WordNetAugmenter()

# Function to augment a single row (scenario and witness)
def augment_row(scenario, witnesses):
    augmented_scenario = augmenter.augment(scenario)
    augmented_witnesses = augmenter.augment(witnesses)
    
    return augmented_scenario, augmented_witnesses

# Load your dataset
df = pd.read_excel(r'C:\Users\hp-15\Disc D\University Files\fifth semester\DL\Deep_Learning_Project\web_scraper\check-judgement.xlsx')

# Augment the data
augmented_data = []
for index, row in df.iterrows():
    scenario = row['scenario']
    witnesses = row['witnesses']
    judgement = row['judgment']
    
    # Add the original row
    augmented_data.append([scenario, witnesses, judgement])
    
    # Create 3 augmented versions
    for _ in range(3):  # You can adjust the number of augmentations
        augmented_scenario, augmented_witnesses = augment_row(scenario, witnesses)
        augmented_data.append([augmented_scenario, augmented_witnesses, judgement])

# Convert the augmented data back to a DataFrame
augmented_df = pd.DataFrame(augmented_data, columns=['scenario', 'witnesses', 'judgment'])

# Optionally, save to a new file
augmented_df.to_excel("augmented_data_textattack.xlsx", index=False)

print(f"Original data had {len(df)} rows, augmented data has {len(augmented_df)} rows.")
