import face_recognition

def load_face_encodings(image_files):
    known_face_encodings = []
    known_face_names = []

    for image_file in image_files:
        image = face_recognition.load_image_file(image_file)
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(image_file.split('/')[-1].split('.')[0])  # Assuming file name is the person's name

    return known_face_encodings, known_face_names

def recognize_faces_in_image(unknown_image_path, known_face_encodings, known_face_names):
    # Load the unknown image
    unknown_image = face_recognition.load_image_file(unknown_image_path)
    unknown_face_encodings = face_recognition.face_encodings(unknown_image)

    names = []
    for unknown_face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding)
        
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        names.append(name)

    return names

# Example usage
known_image_files = ['path/to/person1.jpg', 'path/to/person2.jpg']  # Add paths to known images
known_encodings, known_names = load_face_encodings(known_image_files)

unknown_image_path = 'path/to/unknown_image.jpg'  # Add path to unknown image
detected_names = recognize_faces_in_image(unknown_image_path, known_encodings, known_names)

print("Detected names:", detected_names)
