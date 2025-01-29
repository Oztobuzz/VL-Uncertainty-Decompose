from util.visual_description import *
from benchmark import *
from tqdm import tqdm
import os
from util.misc import *
import json
import argparse


BENCHMARK_TYPE = {
    'MMVet': 'FREE_FORM',
    'LLaVABench': 'FREE_FORM',
    'MMMU': 'MULTI_CHOICE',
    'ScienceQA': 'MULTI_CHOICE'
}

BENCHMARK_MAP = {
    'MMVet': MMVet,
    'LLaVABench': LLaVABench,
    'MMMU': MMMU,
    'ScienceQA': ScienceQA
}

def parse_args():
    parser = argparse.ArgumentParser()
    # parser.add_argument('--lvlm', type=str, default='Qwen2-VL-2B-Instruct')
    parser.add_argument('--benchmark', type=str, default='MMVet')
    parser.add_argument('--benchmark_size', type=int, default= 2)
    parser.add_argument('--prompt_template', type=int, default= 3)
    args = parser.parse_args()
    return args

def obtain_benchmark(args):
    benchmark_class = BENCHMARK_MAP.get(args.benchmark)
    if not benchmark_class:
        raise ValueError(f"Unsupported benchmark: {args.benchmark}")
    return benchmark_class()


def obtain_single_sample(args, benchmark, idx, log_dict, prompt):
    sample = benchmark.retrieve(idx)
    print(sample)
    log_dict[idx]['question'] = sample['question']
    try:
        log_dict[idx]['image_description'] = create_visual_description(sample, prompt)
    except Exception as e:
        log_dict[idx]['image_description'] = str(e)
    log_dict[idx]['gt_ans'] = sample['gt_ans']
        # print(f'{idx} Error: {e}')
    log_dict[idx]['gt_ans'] = sample['gt_ans']
    return None 

def handle_batch(args, benchmark):
    log_dict = {}
    log_dict['args'] = str(args)
    log_dict['benchmark'] = args.benchmark
    benchmark_size = benchmark.obtain_size()
    print(f'- Benchmark size: {benchmark_size}.')
    benchmark_size = args.benchmark_size if args.benchmark_size < benchmark_size else benchmark_size
    print(f'- Test size: {benchmark_size}.')
    log_dict['benchmark_size'] = benchmark_size
    prompt = get_prompt_template(load_prompt_template(), args.prompt_template)
    log_dict['prompt_template'] = prompt 
    for idx in tqdm(range(benchmark_size)):
        log_dict[idx] = {}
        try:
            handle_single(args, idx, benchmark, log_dict, prompt)
            if(idx % 10 == 0):
                save_log(log_dict, args)
        except Exception as e:
            log_dict[idx]['error'] = str(e)
            print(f'{idx} Error: {e}')
    save_log(log_dict, args)
        

def save_log(log_dict, args):
    if not os.path.exists('image_descriptions'):
        os.makedirs('image_descriptions')
    with open(f'image_descriptions/{log_dict["benchmark"]}_{get_cur_time()}_prompt{args.prompt_template}.json', "w", encoding='utf-8') as f: 
        json.dump(log_dict, f, ensure_ascii=False, indent=4)
    print(f'- Full log is saved at image_descriptions/{log_dict["benchmark"]}_{get_cur_time()}_prompt{args.prompt_template}.json.')
        
        
def handle_single(args, idx, benchmark, log_dict, prompt):
    sample = obtain_single_sample(args, benchmark, idx, log_dict, prompt)
    

def main():
    args = parse_args()
    benchmark = obtain_benchmark(args)
    handle_batch(args, benchmark)

if __name__ == "__main__":
    main()