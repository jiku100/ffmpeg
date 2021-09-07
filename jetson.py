import ffmpeg
import pandas as pd
import time
import os 

OUTPUTNAME = "out.mp4"
CODECS = {'h264': 'h264', 'h265': 'hevc'}
TARGETS = ['QP', 'CRF']

if not os.path.exists("./csv_files"):
    os.mkdir("./csv_files")


for codec in CODECS.keys():   
    for target in TARGETS:
        csv_file_header = "./csv_files/" + codec + "_" + target
        csv_file_size_name = csv_file_header + "_" + "FileSize.csv"
        csv_encoding_time_name = csv_file_header + "_" + "EncodingTime.csv"

        index_list = [target + str(i) for i in range(48,52)]
        file_size_index = index_list.copy()
        file_size_index.insert(0, "RAW")
        encoding_time_index = index_list.copy()

        df_file_size = pd.DataFrame(index=file_size_index)
        df_encoding_time = pd.DataFrame(index=encoding_time_index)

        for i in range(1, 3):
            input_file_name = "./original/" + "subject" + str(i) + "/vid.avi"
            encoding_times = []
            video_sizes = []
            video_sizes.append(os.path.getsize(input_file_name))
            for quality in range(48, 52):
                encoding_time = 0
                if target == "QP":
                    encoding_start = time.time()
                    (
                        ffmpeg
                        .input(input_file_name)
                        .output(OUTPUTNAME, qp = quality, vcodec = CODECS[codec])
                        .overwrite_output()
                        .run(quiet=True)
                    )
                    encoding_time = time.time() - encoding_start
                else:
                    encoding_start = time.time()
                    (
                        ffmpeg
                        .input(input_file_name)
                        .output(OUTPUTNAME, crf = quality, vcodec = CODECS[codec])
                        .overwrite_output()
                        .run(quiet=True)
                    )
                    encoding_time = time.time() - encoding_start
                encoding_times.append(encoding_time)
                MB_file_size = os.path.getsize(OUTPUTNAME) / (1024 * 1024)
                video_sizes.append(MB_file_size)

            column_name = "subject" + str(i)
            df_file_size[column_name] = video_sizes
            df_encoding_time[column_name] = encoding_times

        df_file_size.index.name = "Quality"
        df_encoding_time.index.name = "Quality"

        df_file_size.to_csv(csv_file_size_name)
        df_encoding_time.to_csv(csv_encoding_time_name)