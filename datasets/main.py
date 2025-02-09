import os, random

def rename_files(directory):
    # List files in the directory
    files = os.listdir(directory)

    # Rename files
    for filename in files:
        old_path = os.path.join(directory, filename)
        zeros = ""
        for _ in range(5-len(filename[6:-4])):
            zeros += "0"
        new_name = filename[:6] + zeros + filename[6:-4] + filename[-4:]
        new_path = os.path.join(directory, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")

def split(train, val, test):
    labels = os.listdir("datasets/labels/")
    images = os.listdir("datasets/images/")
    pairs = []

    for image in images:
        if image[:-4] + ".txt" in labels:
            pairs.append([image, image[:-4] + ".txt"])

    print(len(labels))
    print(len(images))
    print(len(pairs))

    random.shuffle(pairs)

    train_count = int(train * len(pairs))
    val_count = int(val * len(pairs))
    test_count = int(test * len(pairs))
    print(train_count,
          val_count,
          test_count,
          len(pairs),
          train_count+val_count+test_count)
    
    # Create directories
    for split_name in ["train", "val", "test"]:
        for subfolder in ["images", "labels"]:
            os.makedirs(os.path.join("datasets/hornets_2", split_name, subfolder), exist_ok=True)
    
    # Fill directories based on rations
    for image, label in pairs:
        if train_count > 0:
            os.rename("datasets/labels/" + label, "datasets/hornets_2/train/labels/" + label)
            os.rename("datasets/images/" + image, "datasets/hornets_2/train/images/" + image)
            train_count -= 1
            continue

        if val_count > 0:
            os.rename("datasets/labels/" + label, "datasets/hornets_2/val/labels/" + label)
            os.rename("datasets/images/" + image, "datasets/hornets_2/val/images/" + image)
            val_count -= 1
            continue

        if test_count > 0:
            os.rename("datasets/labels/" + label, "datasets/hornets_2/test/labels/" + label)
            os.rename("datasets/images/" + image, "datasets/hornets_2/test/images/" + image)
            test_count -= 1
            continue

# rename_files("labels/")
# rename_files("datasets/images/")
split(0.9, 0.05, 0.05)