"""Transparent lexical checks for saved question-answer runs, not an LLM judge."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

def tokens(text):
    return re.findall(r'[a-z0-9]+', text.lower())

def token_f1(answer, expected):
    a, b = Counter(tokens(answer)), Counter(tokens(expected))
    if not a or not b:
        return float(a == b)
    common = sum((a & b).values())
    if not common:
        return 0.0
    precision, recall = common/sum(a.values()), common/sum(b.values())
    return 2*precision*recall/(precision+recall)

def evaluate(rows):
    if not isinstance(rows, list) or not rows:
        raise ValueError('Input must be a nonempty JSON array.')
    results, seen = [], set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f'Row {index+1} must be an object.')
        for key in ('id', 'question', 'answer', 'expected_answer'):
            if not isinstance(row.get(key), str) or not row[key].strip():
                raise ValueError(f'Row {index+1}: {key} must be a nonempty string.')
        if row['id'] in seen:
            raise ValueError('Duplicate row id: '+row['id'])
        seen.add(row['id'])
        for key in ('retrieved_sources', 'expected_sources'):
            value = row.get(key)
            if not isinstance(value, list) or not all(isinstance(s, str) and s.strip() for s in value):
                raise ValueError(f'Row {index+1}: {key} must be a list of source strings.')
        expected = set(row['expected_sources'])
        retrieved = set(row['retrieved_sources'])
        recall = len(expected & retrieved)/len(expected) if expected else None
        results.append({'id': row['id'],
            'normalized_exact_match': tokens(row['answer']) == tokens(row['expected_answer']),
            'answer_token_f1': token_f1(row['answer'], row['expected_answer']),
            'source_recall': recall})
    recalls = [r['source_recall'] for r in results if r['source_recall'] is not None]
    return {'count': len(results),
        'mean_exact_match': sum(r['normalized_exact_match'] for r in results)/len(results),
        'mean_answer_token_f1': sum(r['answer_token_f1'] for r in results)/len(results),
        'mean_source_recall': sum(recalls)/len(recalls) if recalls else None,
        'rows_with_expected_sources': len(recalls), 'results': results}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?', default=str(Path(__file__).parent/'data/sample_runs.json'))
    parser.add_argument('--output', help='Optional report path; existing file is replaced')
    args = parser.parse_args()
    try:
        report = evaluate(json.loads(Path(args.input).read_text(encoding='utf-8')))
        rendered = json.dumps(report, indent=2)
        if args.output:
            if Path(args.output).resolve() == Path(args.input).resolve():
                raise ValueError('Output must differ from input.')
            Path(args.output).write_text(rendered+'\n', encoding='utf-8')
        print(rendered)
    except (ValueError, OSError) as exc:
        parser.exit(1, f'Error: {exc}\n')

if __name__ == '__main__':
    main()
