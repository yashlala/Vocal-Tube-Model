import json

vocalTubeLength = 17 #centimeter length of the vocal tube

#area search range in cm^2
areaLow = 1
areaHigh = 10

#length search range in cm
lengthLow = 3

lengthStride = 1 #cm
areaStride = 1 #cm^2

tube_values = {}

i = 0

#Search loop for 2 tube model
tube1_area = areaLow
while tube1_area <= areaHigh:
	tube2_area = areaLow
	while tube2_area <= areaHigh:
		tube1_length = lengthLow
		#We have one loop for length (we have 1 free parameter, since tube length is fixed)
		while tube1_length <= vocalTubeLength:
			i += 1

			tube2_length = vocalTubeLength - tube1_length

			if not (tube1_length >= lengthLow and tube2_length >= lengthLow):
				tube1_length += lengthStride
				continue

			label = "_".join([str(tube1_length), str(tube1_area), str(tube2_length), str(tube2_area)])
			tube_values[label] = [[tube1_length, tube1_area], [tube2_length, tube2_area]]

			tube1_length += lengthStride
		tube2_area += areaStride
	tube1_area += areaStride

print("[INFO] Generated", len(tube_values), "tube configurations")

config_file = "config.json"
with open(config_file, 'r') as f:
	config = json.load(f)
config["tube_values"] = tube_values
with open(config_file, 'w') as f:
	json.dump(config, f, indent=4)
print("[INFO] Saved to", config_file)