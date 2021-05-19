def kafkaSendFiles(
    directories, files, basicmetadata, df_metadata, kafkaProducer, kafkaTopic
):

    import hashlib
    from PIL import Image
    import os
    from kafka import KafkaProducer

    blobstorage_dir = directories["blobstorage_dir"]
    thumbnail_dir = directories["thumbnail_dir"]
    ingest_dir = directories["ingest_dir"]

    j = -1
    for filename in files:
        j = j + 1
        filenameOS = filename.replace("\\", "/")
        with open(filenameOS, "rb") as f:
            file_hash = hashlib.md5()
            chunk = f.read(2 ** 13)
            while chunk:
                file_hash.update(chunk)
                chunk = f.read(2 ** 13)

        filenameHash = file_hash.hexdigest()
        f.close()
        image = Image.open(filenameOS).convert("RGB")
        width, height = image.size
        max_w = 400
        factor = max_w / width
        newsize = (int(width * factor), int(height * factor))
        # Write to Blob Storage
        print("Save image into Blob Storage:" + filenameHash)
        image.save(blobstorage_dir + "/" + filenameHash + ".png")
        imageThumb = image.resize(newsize)
        imageThumb.save(thumbnail_dir + "/" + filenameHash + ".jpg")

        relPath = os.path.relpath(filenameOS, ingest_dir)
        relPath = relPath.replace("\\", "/")
        (basedir, name) = os.path.split(relPath)
        newEntry = {
            "datasetprovider": basicmetadata["datasetprovider"],
            "datasetproviderURL": basicmetadata["datasetproviderURL"],
            "datasetname": basicmetadata["datasetname"],
            "datasetcontainer": basicmetadata["datasetcontainer"],
            "imageFilename": name,
            "imageRelativePath": relPath,
            "imageHeight": height,
            "imageWidth": width,
            "filenameHash": filenameHash,
        }
        if "lat" in df_metadata:
            newEntry["lat"] = df_metadata["lat"][j]
        if "lon" in df_metadata:
            newEntry["lon"] = df_metadata["lon"][j]
        if "alt" in df_metadata:
            newEntry["alt"] = df_metadata["alt"][j]
        if "vf" in df_metadata:
            newEntry["velocity_lon"] = df_metadata["vf"][j]
        if "vl" in df_metadata:
            newEntry["velocity_lat"] = df_metadata["vl"][j]
        if "vu" in df_metadata:
            newEntry["velocity_alt"] = df_metadata["vu"][j]
        if "ax" in df_metadata:
            newEntry["acceleration_lon"] = df_metadata["ax"][j]
        if "ay" in df_metadata:
            newEntry["acceleration_lat"] = df_metadata["ay"][j]
        if "az" in df_metadata:
            newEntry["acceleration_alt"] = df_metadata["az"][j]
        if "ts" in df_metadata:
            newEntry["timestamp"] = df_metadata["ts"][j]

        print("Sending ", relPath)
        # kafkaTopic='topic_test'
        kafkaProducer.send(kafkaTopic, value=newEntry)
