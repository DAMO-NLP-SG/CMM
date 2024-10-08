import os
import json

if __name__ == '__main__':
    # open output file
    with open('./output.json', 'r') as f:
        lines = f.readlines()

    ### Overall Accuracy, Perception Accuracy, and Hallucination Resistance for the entire dataset
    total = 0
    correct = 0
    total_yes_in_answer = 0
    correct_yes = 0
    total_no_in_answer = 0
    correct_no = 0

    for line in lines:
        sample = json.loads(line)
        answer = sample['answer'].strip().lower()
        prediction = sample['pred'].strip().lower()
        total += 1
        
        # Check if the prediction is correct (for overall accuracy)
        if answer in prediction[:5]:
            correct += 1

        # Check for "yes" or "no" in the answers
        if 'yes' in answer[:5]:
            total_yes_in_answer += 1
            if 'yes' in prediction[:5]:
                correct_yes += 1
        elif 'no' in answer[:5]:
            total_no_in_answer += 1
            if 'no' in prediction[:5]:
                correct_no += 1

    # Calculate and print overall accuracy, perception accuracy, and Hallucination Resistance for the entire dataset
    overall_accuracy = correct / total if total > 0 else 0
    overall_perception_accuracy = correct_yes / total_yes_in_answer if total_yes_in_answer > 0 else 0
    overall_hallucination_severity = correct_no / total_no_in_answer if total_no_in_answer > 0 else 0

    print(f'Overall Accuracy (entire dataset): {overall_accuracy:.4f}')
    print(f'Overall Perception Accuracy (entire dataset): {overall_perception_accuracy:.4f}')
    print(f'Overall Hallucination Resistance (entire dataset): {overall_hallucination_severity:.4f}\n')

    ### Perception Accuracy, Hallucination Resistance, and Accuracy for each sub_category
    sub_category_dict = {}

    # First loop to accumulate counts for each sub_category
    for line in lines:
        sample = json.loads(line)
        sub_category = sample['sub_category']
        if sub_category not in sub_category_dict:
            sub_category_dict[sub_category] = {
                'correct_yes': 0, 'total_yes_in_answer': 0,  # For perception accuracy
                'correct_no': 0, 'total_no_in_answer': 0,    # For Hallucination Resistance
                'correct': 0, 'total': 0                    # For overall accuracy
            }
        
        answer = sample['answer'].strip().lower()
        prediction = sample['pred'].strip().lower()
        
        # Update total for counting predictions and answers
        sub_category_dict[sub_category]['total'] += 1
        
        # Check for overall accuracy
        if answer in prediction[:5]:
            sub_category_dict[sub_category]['correct'] += 1

        # Check for "yes" or "no" in the answers
        if 'yes' in answer[:5]:
            sub_category_dict[sub_category]['total_yes_in_answer'] += 1
            if 'yes' in prediction[:5]:
                sub_category_dict[sub_category]['correct_yes'] += 1
        elif 'no' in answer[:5]:
            sub_category_dict[sub_category]['total_no_in_answer'] += 1
            if 'no' in prediction[:5]:
                sub_category_dict[sub_category]['correct_no'] += 1

    # Print the combined result in a table format with alignment
    print(f'{"sub_category":<35}{"perception accuracy":<20}{"Hallucination Resistance":<25}{"accuracy":<10}')
    for sub_category in sub_category_dict:
        correct_yes = sub_category_dict[sub_category]['correct_yes']
        total_yes_in_answer = sub_category_dict[sub_category]['total_yes_in_answer']
        correct_no = sub_category_dict[sub_category]['correct_no']
        total_no_in_answer = sub_category_dict[sub_category]['total_no_in_answer']
        correct = sub_category_dict[sub_category]['correct']
        total = sub_category_dict[sub_category]['total']
        
        # Calculate perception accuracy, Hallucination Resistance, and accuracy
        perception_accuracy = correct_yes / total_yes_in_answer if total_yes_in_answer > 0 else 0
        hallucination_severity = correct_no / total_no_in_answer if total_no_in_answer > 0 else 0
        accuracy = correct / total if total > 0 else 0
        
        print(f'{sub_category:<35}{perception_accuracy:<20.4f}{hallucination_severity:<25.4f}{accuracy:<10.4f}')
    
    ### Perception Accuracy, Hallucination Resistance, and Accuracy for object-level and event-level within each sub_category
    granularity_dict = {
        'object-level': {},
        'event-level': {}
    }

    # First loop to accumulate counts for both levels
    for line in lines:
        sample = json.loads(line)
        sub_category = sample['sub_category']
        granularity = sample['granularity']  # Determine the level: object-level or event-level
        
        if granularity not in granularity_dict:
            continue  # Skip if the granularity is not recognized
        
        if sub_category not in granularity_dict[granularity]:
            granularity_dict[granularity][sub_category] = {
                'correct_yes': 0, 'total_yes_in_answer': 0,  # For perception accuracy
                'correct_no': 0, 'total_no_in_answer': 0,    # For Hallucination Resistance
                'correct': 0, 'total': 0                    # For overall accuracy
            }
        
        answer = sample['answer'].strip().lower()
        prediction = sample['pred'].strip().lower()
        
        # Update total for counting predictions and answers
        granularity_dict[granularity][sub_category]['total'] += 1
        
        # Check for overall accuracy
        if answer in prediction[:5]:
            granularity_dict[granularity][sub_category]['correct'] += 1

        # Check for "yes" or "no" in the answers
        if 'yes' in answer[:5]:
            granularity_dict[granularity][sub_category]['total_yes_in_answer'] += 1
            if 'yes' in prediction[:5]:
                granularity_dict[granularity][sub_category]['correct_yes'] += 1
        elif 'no' in answer[:5]:
            granularity_dict[granularity][sub_category]['total_no_in_answer'] += 1
            if 'no' in prediction[:5]:
                granularity_dict[granularity][sub_category]['correct_no'] += 1

    # Print the combined result for both levels in a table format with alignment
    print(f'\n{"Granularity":<15}{"sub_category":<35}{"perception accuracy":<20}{"Hallucination Resistance":<25}{"accuracy":<10}')
    for granularity in granularity_dict:
        print(f'{granularity.upper()} RESULTS:')
        for sub_category in granularity_dict[granularity]:
            correct_yes = granularity_dict[granularity][sub_category]['correct_yes']
            total_yes_in_answer = granularity_dict[granularity][sub_category]['total_yes_in_answer']
            correct_no = granularity_dict[granularity][sub_category]['correct_no']
            total_no_in_answer = granularity_dict[granularity][sub_category]['total_no_in_answer']
            correct = granularity_dict[granularity][sub_category]['correct']
            total = granularity_dict[granularity][sub_category]['total']
            
            # Calculate perception accuracy, Hallucination Resistance, and accuracy
            perception_accuracy = correct_yes / total_yes_in_answer if total_yes_in_answer > 0 else 0
            hallucination_severity = correct_no / total_no_in_answer if total_no_in_answer > 0 else 0
            accuracy = correct / total if total > 0 else 0
            
            print(f'{granularity:<15}{sub_category:<35}{perception_accuracy:<20.4f}{hallucination_severity:<25.4f}{accuracy:<10.4f}')
