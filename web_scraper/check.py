# !pip install textattack --quiet # Install TextAttack 
from textattack.augmentation import WordNetAugmenter, ParaphraseAugmenter


augmenter = ParaphraseAugmenter()
augmented_text = augmenter.augment("The car was speeding down the street.")
print(augmented_text)
