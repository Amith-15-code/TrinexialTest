#!/usr/bin/env python3
"""
Email service for Trinexial Technologies Mock Aptitude Test
Sends scorecard details to candidates via Gmail SMTP
"""

import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Any

class TrinexialEmailService:
    def __init__(self):
        # Gmail SMTP configuration
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "amithvenkatesh223@gmail.com"
        self.sender_password = os.getenv("GMAIL_APP_PASSWORD")  # Use App Password for security
        
    def create_scorecard_email(self, user_data: Dict[str, Any], score_data: Dict[str, Any]) -> str:
        """Create HTML email template with scorecard details"""
        
        name = user_data.get('name', 'Candidate')
        email = user_data.get('email', '')
        roll = user_data.get('roll', 'N/A')
        
        score = score_data.get('score', 0)
        total = score_data.get('total', 0)
        percentage = round((score / total) * 100, 2) if total > 0 else 0
        violations = score_data.get('violations', 0)
        
        # Performance assessment
        if percentage >= 90:
            performance = "Excellent"
            grade_color = "#28a745"
        elif percentage >= 80:
            performance = "Very Good"
            grade_color = "#17a2b8"
        elif percentage >= 70:
            performance = "Good"
            grade_color = "#ffc107"
        elif percentage >= 60:
            performance = "Satisfactory"
            grade_color = "#fd7e14"
        else:
            performance = "Needs Improvement"
            grade_color = "#dc3545"
        
        # Subject-wise breakdown (mock data based on question categories)
        subject_breakdown = {
            "Digital Electronics": {"correct": 0, "total": 0},
            "VLSI": {"correct": 0, "total": 0},
            "DSP": {"correct": 0, "total": 0},
            "DC (Circuits)": {"correct": 0, "total": 0},
            "Aptitude": {"correct": 0, "total": 0}
        }
        
        # Count correct answers by subject (simplified - would need actual question mapping)
        questions = score_data.get('questions', [])
        answers = score_data.get('answers', [])
        
        for i, question in enumerate(questions):
            if i < len(answers) and answers[i] == question.get('a', -1):
                subject = question.get('c', 'General')
                if subject in subject_breakdown:
                    subject_breakdown[subject]["correct"] += 1
                subject_breakdown[subject]["total"] += 1
        
        # Generate subject breakdown HTML
        subject_html = ""
        for subject, data in subject_breakdown.items():
            if data["total"] > 0:
                sub_percentage = round((data["correct"] / data["total"]) * 100, 1)
                subject_html += f"""
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #e9ecef;">{subject}</td>
                    <td style="padding: 8px; border-bottom: 1px solid #e9ecef; text-align: center;">{data['correct']}/{data['total']}</td>
                    <td style="padding: 8px; border-bottom: 1px solid #e9ecef; text-align: center; color: {grade_color};">{sub_percentage}%</td>
                </tr>
                """
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #5b8cff, #8b5bff); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
                .scorecard {{ background: white; border-radius: 10px; padding: 25px; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .score {{ font-size: 48px; font-weight: bold; color: {grade_color}; text-align: center; margin: 20px 0; }}
                .performance {{ text-align: center; font-size: 18px; color: {grade_color}; margin-bottom: 30px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th {{ background: #e9ecef; padding: 12px; text-align: left; font-weight: bold; }}
                .footer {{ text-align: center; margin-top: 30px; color: #6c757d; font-size: 14px; }}
                .highlight {{ background: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Trinexial Technologies</h1>
                    <h2>Mock Aptitude Test - Scorecard</h2>
                </div>
                
                <div class="content">
                    <p>Dear <strong>{name}</strong>,</p>
                    
                    <p>Thank you for taking the Trinexial Technologies Mock Aptitude Test. We are pleased to share your detailed scorecard and performance analysis.</p>
                    
                    <div class="scorecard">
                        <h3 style="text-align: center; margin-bottom: 20px;">Your Scorecard</h3>
                        
                        <div class="score">{score}/{total}</div>
                        <div class="performance">{performance} ({percentage}%)</div>
                        
                        <table>
                            <tr>
                                <th>Subject</th>
                                <th style="text-align: center;">Score</th>
                                <th style="text-align: center;">Percentage</th>
                            </tr>
                            {subject_html}
                        </table>
                        
                        <div style="margin-top: 20px;">
                            <p><strong>Test Details:</strong></p>
                            <ul>
                                <li>Candidate ID: {roll}</li>
                                <li>Test Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</li>
                                <li>Total Questions: {total}</li>
                                <li>Correct Answers: {score}</li>
                                <li>Proctoring Violations: {violations}</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="highlight">
                        <h4>Next Steps</h4>
                        <p>Based on your performance, our team will review your results and contact you within 2-3 business days regarding the next phase of our selection process.</p>
                        <p>If you have any questions about your results, please don't hesitate to reach out to us.</p>
                    </div>
                    
                    <p>We appreciate your interest in Trinexial Technologies and wish you the best of luck!</p>
                    
                    <div class="footer">
                        <p><strong>Trinexial Technologies</strong><br>
                        Email: amithvenkatesh223@gmail.com<br>
                        <em>Innovating the Future of Technology</em></p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def send_scorecard_email(self, user_data: Dict[str, Any], score_data: Dict[str, Any]) -> bool:
        """Send scorecard email to candidate"""
        
        if not self.sender_password:
            print("Error: Gmail App Password not set. Please set GMAIL_APP_PASSWORD environment variable.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = user_data.get('email', '')
            msg['Subject'] = f"Trinexial Technologies - Mock Aptitude Test Scorecard for {user_data.get('name', 'Candidate')}"
            
            # Create HTML content
            html_content = self.create_scorecard_email(user_data, score_data)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"Scorecard email sent successfully to {user_data.get('email')}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

def send_test_scorecard(user_data: Dict[str, Any], score_data: Dict[str, Any]) -> bool:
    """Convenience function to send scorecard email"""
    email_service = TrinexialEmailService()
    return email_service.send_scorecard_email(user_data, score_data)

if __name__ == "__main__":
    # Test email functionality
    test_user = {
        "name": "John Doe",
        "email": "test@example.com",
        "roll": "EE23-001"
    }
    
    test_score = {
        "score": 12,
        "total": 15,
        "answers": [0, 1, 2, 1, 0, 2, 1, 0, 1, 2, 0, 1, 2, 1, 0],
        "questions": [
            {"c": "Digital Electronics", "a": 0},
            {"c": "Digital Electronics", "a": 1},
            {"c": "VLSI", "a": 2},
            {"c": "VLSI", "a": 1},
            {"c": "DSP", "a": 0},
            {"c": "DSP", "a": 2},
            {"c": "DC (Circuits)", "a": 1},
            {"c": "DC (Circuits)", "a": 0},
            {"c": "Aptitude", "a": 1},
            {"c": "Aptitude", "a": 2},
            {"c": "Digital Electronics", "a": 0},
            {"c": "DSP", "a": 1},
            {"c": "VLSI", "a": 2},
            {"c": "DC (Circuits)", "a": 1},
            {"c": "Aptitude", "a": 0}
        ],
        "violations": 1
    }
    
    print("Testing email service...")
    success = send_test_scorecard(test_user, test_score)
    print(f"Email sent: {success}")
