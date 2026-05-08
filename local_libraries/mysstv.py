from local_libraries.sstv_library.sstv import SSTVDecoder

def decode():
	with SSTVDecoder("output.wav") as decoder:
		img = decoder.decode()
		if img is None:
			print("No SSTV signal found in audio file")
		img.save("attachement.png")

