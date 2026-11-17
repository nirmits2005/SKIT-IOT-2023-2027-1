#!/usr/bin/env python3
"""
Network Intrusion Detection System (NIDS) - Progress Report Generator (Form-3)
Based on the official FlowStock Form-3 ReportLab reference implementation.

Supports:
- python generate_report.py weekly
- python generate_report.py monthly
- python generate_report.py final
- python generate_report.py --start-date YYYY-MM-DD --end-date YYYY-MM-DD [--output FILENAME.pdf] [--retrospective]
- python generate_report.py historical (generates reports for all 13 confirmed reporting periods)
"""

import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
import argparse
import subprocess
from collections import defaultdict
import datetime
import io
import sys
import html
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# -------------------------------------------------------------
# CONFIGURATION: Institution & Department Details
# -------------------------------------------------------------
COLLEGE_NAME = "Swami Keshvanand Institute of Technology,Management & Gramothan, Jaipur"
DEPARTMENT_NAME = "Department of Computer Science & Engineering"
PROJECT_NAME = "Network Intrusion Detection System (NIDS)"

# Canonical team members
CANONICAL_TEAM = [
    "Shobhan Bhagwati",
    "Nitesh Sharma",
    "Shaurya Shekhawat",
    "Prankur Sharma"
]

# Alias mapping for git author identification
AUTHOR_ALIASES = {
    "nitesh sharma": "Nitesh Sharma",
    "nirmits2005": "Nitesh Sharma",
    "nirmit": "Nitesh Sharma",
    "shaurya shekhawat": "Shaurya Shekhawat",
    "shaurya-pratap": "Shaurya Shekhawat",
    "shauryapratap": "Shaurya Shekhawat",
    "shobhan bhagwati": "Shobhan Bhagwati",
    "shobhan": "Shobhan Bhagwati",
    "prankur sharma": "Prankur Sharma",
    "prankur": "Prankur Sharma",
}

# Confirmed 13 Reporting Periods (Chronological DD/MM/YYYY interpretation)
CONFIRMED_PERIODS = [
    ("Period 01", "2026-04-01", "2026-04-09", "NIDS_Weekly_Progress_Report_Form-3_Period_01_2026-04-09.pdf"),
    ("Period 02", "2026-04-10", "2026-08-14", "NIDS_Weekly_Progress_Report_Form-3_Period_02_2026-08-14.pdf"),
    ("Period 03", "2026-08-15", "2026-08-22", "NIDS_Weekly_Progress_Report_Form-3_Period_03_2026-08-22.pdf"),
    ("Period 04", "2026-08-23", "2026-08-29", "NIDS_Weekly_Progress_Report_Form-3_Period_04_2026-08-29.pdf"),
    ("Period 05", "2026-08-30", "2026-09-18", "NIDS_Weekly_Progress_Report_Form-3_Period_05_2026-09-18.pdf"),
    ("Period 06", "2026-09-19", "2026-09-25", "NIDS_Weekly_Progress_Report_Form-3_Period_06_2026-09-25.pdf"),
    ("Period 07", "2026-09-26", "2026-10-02", "NIDS_Weekly_Progress_Report_Form-3_Period_07_2026-10-02.pdf"),
    ("Period 08", "2026-10-03", "2026-10-16", "NIDS_Weekly_Progress_Report_Form-3_Period_08_2026-10-16.pdf"),
    ("Period 09", "2026-10-17", "2026-10-23", "NIDS_Weekly_Progress_Report_Form-3_Period_09_2026-10-23.pdf"),
    ("Period 10", "2026-10-24", "2026-10-30", "NIDS_Weekly_Progress_Report_Form-3_Period_10_2026-10-30.pdf"),
    ("Period 11", "2026-10-31", "2026-11-05", "NIDS_Weekly_Progress_Report_Form-3_Period_11_2026-11-05.pdf"),
    ("Period 12", "2026-11-06", "2026-11-09", "NIDS_Weekly_Progress_Report_Form-3_Period_12_2026-11-09.pdf"),
    ("Period 13", "2026-11-10", "2026-11-12", "NIDS_Weekly_Progress_Report_Form-3_Period_13_2026-11-12.pdf"),
]

def resolve_author(author_raw):
    """Maps git author names to canonical team members."""
    cleaned = author_raw.strip().lower()
    return AUTHOR_ALIASES.get(cleaned, author_raw.strip())

def get_repo_info():
    """Extracts repository name and branch reliably."""
    repo_name = "SKIT-IOT-2023-2027-1"
    branch_name = "main"
    try:
        root_path = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], encoding='utf-8').strip()
        repo_name = os.path.basename(root_path)
    except Exception:
        try:
            remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], encoding='utf-8').strip()
            repo_name = remote_url.rstrip('/').split('/')[-1].replace('.git', '')
        except Exception:
            repo_name = os.path.basename(os.getcwd())
    try:
        branch_name = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], encoding='utf-8').strip()
    except Exception:
        pass
    return repo_name, branch_name

def get_git_metrics(interval="weekly", start_date=None, end_date=None, retrospective=False):
    """
    Parses Git commit logs with accurate filtering and four-member tracking.
    """
    today = datetime.date.today()
    git_args = ['git', 'log', '--no-merges', '--pretty=format:COMMIT|||%h|||%an|||%ad|||%s', '--date=short', '--numstat']
    
    if start_date and end_date:
        git_args.append(f"--since={start_date} 00:00:00")
        git_args.append(f"--until={end_date} 23:59:59")
        scope_title = f"{start_date} to {end_date}"
        if retrospective:
            scope_title += " (Retrospective Progress Window)"
    elif interval == "weekly":
        since_date = (today - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        git_args.append(f"--since={since_date}")
        scope_title = f"Last 7 Days (Since {since_date})"
    elif interval == "monthly":
        since_date = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        git_args.append(f"--since={since_date}")
        scope_title = f"Last 30 Days (Since {since_date})"
    else:
        scope_title = "Complete Project Lifecycle (All Commits)"
    
    try:
        raw_output = subprocess.check_output(git_args, encoding='utf-8', errors='replace')
    except subprocess.CalledProcessError:
        print("[ERROR] Git command failed. Please ensure you are inside a Git repository.")
        return None, None, None, scope_title

    # Initialize all 4 canonical members so everyone is tracked
    students = defaultdict(lambda: {"commits": 0, "added": 0, "deleted": 0, "active_days": set()})
    for m in CANONICAL_TEAM:
        students[m] = {"commits": 0, "added": 0, "deleted": 0, "active_days": set()}

    timeline_activity = defaultdict(lambda: defaultdict(int))
    student_logs = defaultdict(list)
    current_author = None
    current_date_str = None

    for line in raw_output.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('COMMIT|||'):
            parts = line.split('|||')
            if len(parts) >= 5:
                sha = parts[1].strip()
                raw_author = parts[2].strip()
                date_str = parts[3].strip()
                msg = parts[4].strip()
            else:
                continue
                
            # --- IGNORE AUTOMATED BOTS ---
            if "bot" in raw_author.lower() or "github-actions" in raw_author.lower():
                current_author = None
                continue
            # -----------------------------
            
            current_author = resolve_author(raw_author)
            current_date_str = date_str
            
            students[current_author]["commits"] += 1
            students[current_author]["active_days"].add(current_date_str)
            student_logs[current_author].append((date_str, sha, msg))
            
            try:
                dt = datetime.datetime.strptime(current_date_str, "%Y-%m-%d").date()
                if interval in ("weekly", "historical") or (start_date and end_date):
                    period_key = dt.strftime("%a (%b %d)")
                elif interval == "monthly":
                    period_key = f"{dt.isocalendar()[0]}-W{dt.isocalendar()[1]:02d}"
                else:
                    period_key = dt.strftime("%Y-%m")
                timeline_activity[period_key][current_author] += 1
            except Exception:
                pass
        elif current_author and not line.startswith('COMMIT|||'):
            parts = line.split()
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                students[current_author]["added"] += int(parts[0])
                students[current_author]["deleted"] += int(parts[1])

    return students, timeline_activity, student_logs, scope_title

def create_charts(students, timeline_activity, interval):
    """Generates visual workload and trend charts."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.8))
    
    # 1. Timeline Line Chart
    has_activity = any(data["commits"] > 0 for data in students.values())
    periods = sorted(timeline_activity.keys())
    active_authors = [a for a in CANONICAL_TEAM if students[a]["commits"] > 0]
    
    if periods and active_authors:
        for author in active_authors:
            counts = [timeline_activity[p].get(author, 0) for p in periods]
            ax1.plot(periods, counts, marker='o', linewidth=2, label=author)
        ax1.set_title(f"Commit Timeline ({interval.capitalize()})", fontsize=10, fontweight='bold')
        ax1.set_ylabel("Commits")
        ax1.tick_params(axis='x', rotation=30)
        ax1.grid(True, linestyle='--', alpha=0.5)
        ax1.legend(fontsize=8)
    else:
        ax1.text(0.5, 0.5, "No commits found in this interval", ha='center', va='center', fontsize=9, color='#64748B')
        ax1.set_title("Commit Timeline", fontsize=10, fontweight='bold')
        ax1.set_xticks([])
        ax1.set_yticks([])

    # 2. Net LOC Bar Chart across 4 team members
    authors = CANONICAL_TEAM
    net_loc = [students[a]["added"] - students[a]["deleted"] for a in authors]
    colors_list = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2']
    
    ax2.bar(authors, net_loc, color=colors_list[:len(authors)], width=0.45)
    ax2.set_title("Net Lines of Code Written", fontsize=10, fontweight='bold')
    ax2.set_ylabel("LOC (Added - Deleted)")
    ax2.tick_params(axis='x', rotation=20, labelsize=7.5)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=200)
    plt.close()
    img_buffer.seek(0)
    return Image(img_buffer, width=500, height=170)

def generate_pdf(interval="weekly", start_date=None, end_date=None, output_filename=None, retrospective=False):
    repo_name, branch_name = get_repo_info()
    students, timeline_activity, student_logs, scope_title = get_git_metrics(
        interval=interval, start_date=start_date, end_date=end_date, retrospective=retrospective
    )
    if students is None:
        return None

    date_stamp = datetime.date.today().strftime("%Y-%m-%d")
    
    if output_filename:
        doc_name = output_filename
        if interval == "weekly":
            report_title = "Weekly Progress Report (Form-3)"
        elif interval == "monthly":
            report_title = "Monthly Progress Report (Form-3)"
        elif interval == "final":
            report_title = "Final Project Evaluation Report (Form-3)"
        else:
            report_title = "Progress Report (Form-3)"
    elif interval == "weekly":
        report_title = "Weekly Progress Report (Form-3)"
        doc_name = f"{repo_name}_Weekly_Progress_Report_Form-3_{date_stamp}.pdf"
    elif interval == "monthly":
        report_title = "Monthly Progress Report (Form-3)"
        doc_name = f"{repo_name}_Monthly_Progress_Report_Form-3_{date_stamp}.pdf"
    elif interval == "final":
        report_title = "Final Project Evaluation Report (Form-3)"
        doc_name = f"{repo_name}_Final_Report_{date_stamp}.pdf"
    else:
        report_title = "Progress Report (Form-3)"
        doc_name = f"{repo_name}_Report_{date_stamp}.pdf"

    # Make parent directory if needed
    parent_dir = os.path.dirname(doc_name)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    doc = SimpleDocTemplate(
        doc_name,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=30,
        bottomMargin=30
    )
    styles = getSampleStyleSheet()
    
    college_style = ParagraphStyle(
        'CollegeStyle', parent=styles['Heading1'],
        fontSize=13.5, leading=17, textColor=colors.HexColor("#0F172A"), alignment=1, spaceAfter=2
    )
    dept_style = ParagraphStyle(
        'DeptStyle', parent=styles['Normal'],
        fontSize=9.5, leading=13, textColor=colors.HexColor("#475569"), alignment=1, spaceAfter=6
    )
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading2'],
        fontSize=13, leading=17, textColor=colors.HexColor("#1A365D"), alignment=1, spaceAfter=5
    )
    repo_style = ParagraphStyle(
        'RepoStyle', parent=styles['Normal'],
        fontSize=9.5, leading=14, textColor=colors.HexColor("#0F172A"), spaceAfter=3
    )
    meta_style = ParagraphStyle(
        'MetaStyle', parent=styles['Normal'],
        fontSize=8.5, textColor=colors.HexColor("#64748B"), spaceAfter=8
    )
    section_style = ParagraphStyle(
        'SectionStyle', parent=styles['Heading2'],
        fontSize=10.5, leading=14, textColor=colors.HexColor("#0F172A"), spaceBefore=7, spaceAfter=4
    )
    sub_section_style = ParagraphStyle(
        'SubSectionStyle', parent=styles['Heading3'],
        fontSize=9, leading=12, textColor=colors.HexColor("#2563EB"), spaceBefore=5, spaceAfter=2
    )
    msg_style = ParagraphStyle(
        'MsgStyle', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=colors.HexColor("#1E293B")
    )
    meta_cell_style = ParagraphStyle(
        'MetaCellStyle', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=colors.HexColor("#475569"), alignment=1
    )
    marks_style = ParagraphStyle(
        'MarksStyle', parent=styles['Normal'],
        fontSize=9, leading=12, textColor=colors.HexColor("#0F172A"), alignment=1
    )
    sig_block_style = ParagraphStyle(
        'SigBlockStyle', parent=styles['Normal'],
        fontSize=9, leading=15, textColor=colors.HexColor("#0F172A"), alignment=0
    )
    story = []

    # 1. Header with College & Department Name and Form-3 Title
    story.append(Paragraph(f"<b>{html.escape(COLLEGE_NAME)}</b>", college_style))
    story.append(Paragraph(f"<b>{html.escape(DEPARTMENT_NAME)}</b>", dept_style))
    story.append(Paragraph(f"<u><b>{report_title}</b></u>", title_style))
    story.append(Spacer(1, 3))

    # 2. Metadata (Repo, Project, Branch, Scope, Date)
    story.append(Paragraph(
        f"<b>Project:</b> <font color='#1A365D'><b>{html.escape(PROJECT_NAME)}</b></font> &nbsp;|&nbsp; "
        f"<b>Repository:</b> <font color='#2563EB'><b>{html.escape(repo_name)}</b></font> &nbsp;|&nbsp; "
        f"<b>Branch:</b> <code>{html.escape(branch_name)}</code>",
        repo_style
    ))
    eval_meta = f"<b>Evaluation Window:</b> {scope_title} &nbsp;|&nbsp; <b>Generated On:</b> {datetime.date.today().strftime('%B %d, %Y')}"
    if retrospective:
        eval_meta += " &nbsp;|&nbsp; <font color='#B45309'><b>[Retrospective Report]</b></font>"
    story.append(Paragraph(eval_meta, meta_style))

    # 3. Individual Summary Table (Four-Member Team)
    story.append(Paragraph("1. Individual Contribution Breakdown (Four-Member Team)", section_style))
    total_commits = sum(data["commits"] for data in students.values())
    table_data = [["Student Name", "Commits (%)", "Lines Added", "Lines Deleted", "Net LOC", "Active Days"]]
    
    # Always display all 4 canonical team members in order
    for name in CANONICAL_TEAM:
        data = students[name]
        pct = (data["commits"] / total_commits * 100) if total_commits > 0 else 0.0
        net = data["added"] - data["deleted"]
        table_data.append([
            html.escape(name),
            f"{data['commits']} ({pct:.1f}%)",
            f"+{data['added']:,}",
            f"-{data['deleted']:,}",
            f"{net:,}",
            f"{len(data['active_days'])} days"
        ])
    
    # Any additional contributors outside canonical team
    for name, data in students.items():
        if name not in CANONICAL_TEAM and data["commits"] > 0:
            pct = (data["commits"] / total_commits * 100) if total_commits > 0 else 0.0
            net = data["added"] - data["deleted"]
            table_data.append([
                html.escape(name),
                f"{data['commits']} ({pct:.1f}%)",
                f"+{data['added']:,}",
                f"-{data['deleted']:,}",
                f"{net:,}",
                f"{len(data['active_days'])} days"
            ])

    table = Table(table_data, colWidths=[120, 80, 80, 80, 80, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(table)
    story.append(Spacer(1, 6))

    # 4. Visual Charts
    story.append(Paragraph("2. Visual Trends & Volume", section_style))
    chart_image = create_charts(students, timeline_activity, interval)
    story.append(chart_image)
    story.append(Spacer(1, 6))

    # 5. Detailed Commit Logs per Student WITH Vertically Merged Mentor Marks
    story.append(Paragraph(f"3. Detailed Commit Logs & Mentor Evaluation", section_style))
    if not student_logs or all(len(logs) == 0 for logs in student_logs.values()):
        empty_note = "<i>No commit logs recorded in Git history for this timeframe.</i>"
        if retrospective:
            empty_note += " (Historical retrospective review period — contributions attributed to module milestones and team responsibilities as documented in TEAM.md)."
        story.append(Paragraph(empty_note, styles['Normal']))
    else:
        for student_name, logs in student_logs.items():
            if not logs:
                continue
            student_section = []
            student_section.append(Paragraph(f"<b>Student:</b> {html.escape(student_name)} — <i>{len(logs)} commit(s)</i>", sub_section_style))
            
            log_table_data = [["Date", "Hash", "Commit Message", "Mentor Marks (/10)"]]
            
            # Place the clean marking line in the first row
            first_date, first_sha, first_msg = logs[0]
            safe_msg = html.escape(first_msg) if first_msg else "(No commit message)"
            log_table_data.append([
                Paragraph(first_date, meta_cell_style),
                Paragraph(f"<code>{first_sha}</code>", meta_cell_style),
                Paragraph(safe_msg, msg_style),
                Paragraph("<b>_____ / 10</b>", marks_style)
            ])
            
            # Subsequent commit rows have blank placeholder for merged cell
            for date_val, sha_val, msg_val in logs[1:]:
                safe_msg = html.escape(msg_val) if msg_val else "(No commit message)"
                log_table_data.append([
                    Paragraph(date_val, meta_cell_style),
                    Paragraph(f"<code>{sha_val}</code>", meta_cell_style),
                    Paragraph(safe_msg, msg_style),
                    ""
                ])
            
            num_rows = len(log_table_data)
            log_table = Table(log_table_data, colWidths=[65, 50, 335, 90])
            
            t_style = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#475569")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (3, 0), (3, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 7.5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
                ('TOPPADDING', (0, 0), (-1, -1), 2.5),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ('ROWBACKGROUNDS', (0, 1), (2, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ('SPAN', (3, 1), (3, num_rows - 1)),
                ('VALIGN', (3, 1), (3, num_rows - 1), 'MIDDLE'),
                ('BACKGROUND', (3, 1), (3, num_rows - 1), colors.HexColor("#FEF3C7")),
            ]
            
            log_table.setStyle(TableStyle(t_style))
            student_section.append(log_table)
            student_section.append(Spacer(1, 5))
            story.append(KeepTogether(student_section))

    # 6. Symmetrical Signatures
    story.append(Spacer(1, 16))
    
    mentor_cell = [
        Paragraph("<b>Name:</b> ___________________________", sig_block_style),
        Paragraph("<b>Designation:</b> Project Mentor", sig_block_style),
        Spacer(1, 6),
        Paragraph("<b>Signature:</b> ________________________", sig_block_style),
    ]
    
    coordinator_cell = [
        Paragraph("<b>Name:</b> ___________________________", sig_block_style),
        Paragraph("<b>Designation:</b> Lab Coordinator", sig_block_style),
        Spacer(1, 6),
        Paragraph("<b>Signature:</b> ________________________", sig_block_style),
    ]
    sig_table = Table([[mentor_cell, coordinator_cell]], colWidths=[270, 270])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, -1), 0),
        ('LEFTPADDING', (1, 0), (1, -1), 40),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    story.append(KeepTogether(sig_table))
    doc.build(story)
    print(f"[SUCCESS] Generated: {doc_name}")
    print(f" -> Tracked {len(CANONICAL_TEAM)} team members and {total_commits} total commits.")
    return doc_name

def generate_all_historical(reports_dir="weekly_reports"):
    """Generates all 13 confirmed historical reports and a consolidated report."""
    os.makedirs(reports_dir, exist_ok=True)
    generated = []
    print("=== Generating 13 Chronological Historical Form-3 PDF Reports ===")
    for idx, (label, start_dt, end_dt, filename) in enumerate(CONFIRMED_PERIODS, 1):
        target_path = os.path.join(reports_dir, filename)
        pdf = generate_pdf(
            interval="historical",
            start_date=start_dt,
            end_date=end_dt,
            output_filename=target_path,
            retrospective=True
        )
        if pdf:
            generated.append(pdf)
    
    # Also generate consolidated Final Project Evaluation Report
    final_path = os.path.join(reports_dir, "NIDS_Final_Project_Evaluation_Report_Form-3.pdf")
    pdf_final = generate_pdf(
        interval="final",
        output_filename=final_path,
        retrospective=False
    )
    if pdf_final:
        generated.append(pdf_final)

    print(f"\n[DONE] Successfully generated {len(generated)} PDF reports in {reports_dir}/")
    return generated

def main():
    parser = argparse.ArgumentParser(description="FlowStock Form-3 PDF Progress Report Generator for NIDS")
    parser.add_argument("interval", nargs="?", default="weekly", choices=["weekly", "monthly", "final", "historical"],
                        help="Reporting interval mode (default: weekly)")
    parser.add_argument("--start-date", dest="start_date", help="Custom start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", dest="end_date", help="Custom end date (YYYY-MM-DD)")
    parser.add_argument("--output", "-o", dest="output", help="Custom PDF output filename")
    parser.add_argument("--retrospective", action="store_true", help="Mark report as retrospective review")
    parser.add_argument("--reports-dir", default="weekly_reports", help="Directory for batch reports")
    args = parser.parse_args()

    if args.interval == "historical":
        generate_all_historical(args.reports_dir)
    elif args.start_date and args.end_date:
        generate_pdf(
            interval="custom",
            start_date=args.start_date,
            end_date=args.end_date,
            output_filename=args.output,
            retrospective=args.retrospective
        )
    else:
        generate_pdf(
            interval=args.interval,
            output_filename=args.output,
            retrospective=args.retrospective
        )

if __name__ == "__main__":
    main()
