import json

def main():
    generations = ["2309gpt3_english", "2309gpt3_german", "2403gpt4_english", "2403gpt4_german", "2409gpt4_english", "2409gpt4_german"]
    for generation in generations:
        print()
        print(f"Generation: {generation}")
        with open(f'../results/{generation}_significant_features_0.01.json') as f:
            data = json.load(f)
            # print the length of each key in the json file
            for key in data:
                for k in data[key]:
                    if k == "bon":
                        print(key, k, len(data[key][k]))

if __name__ == "__main__":
    main()