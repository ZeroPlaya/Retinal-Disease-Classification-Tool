def extract_fov(image):
    np_img = np.array(image)
    gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)

    # Apply Otsu thresholding
    _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Use morphological operations to clean up the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Ensure mask is of type uint8
    mask = mask.astype(np.uint8)

    # Apply the mask to keep only the FOV
    fov_image = cv2.bitwise_and(np_img, np_img, mask=mask)

    return Image.fromarray(fov_image), mask



def load_augmentation_counts(file_path, target_count=100):
    augment_counts = {}
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            disease_combo = row['Disease Combination']
            count = int(row['Count'])
            if count < target_count:
                augment_counts[disease_combo] = target_count - count
    return augment_counts
