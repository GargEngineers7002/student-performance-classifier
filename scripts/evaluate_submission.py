#!/usr/bin/env python3
"""
Script to evaluate student submission for the Student Performance Classifier project.
Checks the judging criteria and assigns points.
"""

import os
import re
import sys

def parse_classification_report(report_text):
    """
    Parse the classification report text to extract accuracy and f1 scores.
    """
    lines = report_text.split('\n')
    accuracy = None
    f1_scores = []

    for line in lines:
        line = line.strip()
        if line.startswith('accuracy'):
            # Extract accuracy
            match = re.search(r'accuracy\s+([\d.]+)', line)
            if match:
                accuracy = float(match.group(1))
        elif re.match(r'\d+', line):  # Lines starting with class number
            parts = line.split()
            if len(parts) >= 4:
                try:
                    f1 = float(parts[3])
                    f1_scores.append(f1)
                except ValueError:
                    pass

    # For binary classification, take the average f1
    f1_avg = sum(f1_scores) / len(f1_scores) if f1_scores else 0

    return accuracy, f1_avg

def check_submission():
    """
    Check the submission folder and evaluate criteria.
    Returns (passed_all, accuracy, f1_score, points, feedback)
    """
    submission_dir = 'submission'
    required_files = [
        'model_performance.txt',
        'confusion_matrix.png',
        'roc_curve.png'
    ]

    feedback = []

    # Check if files exist
    for file in required_files:
        if not os.path.exists(os.path.join(submission_dir, file)):
            feedback.append(f"Missing required file: {file}")
            return False, None, None, 0, feedback

    # Read model_performance.txt
    try:
        with open(os.path.join(submission_dir, 'model_performance.txt'), 'r') as f:
            report_text = f.read()
    except Exception as e:
        feedback.append(f"Error reading model_performance.txt: {e}")
        return False, None, None, 0, feedback

    # Parse metrics
    accuracy, f1_score = parse_classification_report(report_text)

    if accuracy is None:
        feedback.append("Could not parse accuracy from model_performance.txt")
        return False, None, None, 0, feedback

    if f1_score is None:
        feedback.append("Could not parse F1 score from model_performance.txt")
        return False, None, None, 0, feedback

    feedback.append(f"Accuracy: {accuracy:.3f}")
    feedback.append(f"F1 Score: {f1_score:.3f}")

    # Check criteria
    acc_pass = accuracy >= 0.85
    f1_pass = f1_score >= 0.80

    if acc_pass and f1_pass:
        points = 150
        feedback.append("All criteria met! Excellent work.")
    elif acc_pass:
        points = 100
        feedback.append("Accuracy requirement met, but F1 score needs improvement.")
    elif f1_pass:
        points = 75
        feedback.append("F1 score requirement met, but accuracy needs improvement.")
    else:
        points = 50
        feedback.append("Neither accuracy nor F1 score meets requirements. Review your model.")

    passed_all = acc_pass and f1_pass

    return passed_all, accuracy, f1_score, points, feedback

if __name__ == "__main__":
    passed, acc, f1, points, feedback = check_submission()

    print(f"Passed: {passed}")
    print(f"Points: {points}")
    print("Feedback:")
    for msg in feedback:
        print(f"- {msg}")

    # Exit with 0 if passed, 1 if not
    sys.exit(0 if passed else 1)