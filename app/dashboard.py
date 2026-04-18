from __future__ import annotations

import ctypes
import json
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from urllib.parse import urlparse, unquote
import tkinter as tk

#from tkcalendar import DateEntry

def safe_set_dpi_awareness() -> None:
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

def humanize_topic_url(value: str) -> str:
    try:
        parsed = urlparse(value)
        if parsed.scheme and parsed.netloc:
            tail = parsed.path.rstrip("/").split("/")[-1]
            if tail:
                tail = unquote(tail).replace("_", " ")
                return tail
    except Exception:
        pass
    return value

def clean_item(value):
    if isinstance(value, (list, tuple)):
        if len(value) >= 2:
            left = clean_item(value[0])
            right = value[1]
            return f"{left} ({right})"
        if len(value) == 1:
            return clean_item(value[0])
        return "-"

    text = str(value)
    if text.startswith("http://") or text.startswith("https://"):
        text = humanize_topic_url(text)
    return text


def show_results(output_dict):
    """
    Displays the processed stats
    return: Nothing
    """

    stats = output_dict["stats"]
    ai_features = output_dict.get("ai_features", {})
    recommendations = output_dict.get("recommendations", [])
    output_files = output_dict.get("output_files", [])
    ai_insights = output_dict.get("ai_insights", [])
    topic_clusters = output_dict.get("topic_clusters", [])

    safe_set_dpi_awareness()
    root = tk.Tk()
    root.state("zoomed")
    root.title("Watch History Analysis Results")

    canvas = tk.Canvas(root, highlightthickness=0)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    h_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
    scroll_frame = ttk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    scroll_frame.columnconfigure(0, weight=1)
    scroll_frame.columnconfigure(1, weight=1)
    scroll_frame.columnconfigure(2, weight=1)
    scroll_frame.columnconfigure(3, weight=1)
    scroll_frame.columnconfigure(4, weight=1)
    scroll_frame.columnconfigure(5, weight=1)

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set, xscrollcommand=h_scrollbar.set)
    h_scrollbar.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    row = 0
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()

    l_bg_color = "#edebeb"
    l_field_bg_color = "#cecece"
    l_accent1 = "#3F3F3F"
    l_accent2 = "#74EAFF"

    d_bg_color = "#181837"
    d_field_bg_color = "#252652"
    d_accent1 = "#E0E3B0"
    d_accent2 = "#74EAFF"

    fontF = "Ubuntu"
    fontS = 20 * max(1, int(h / 1080))
    value_wrap = max(260, int(w * 0.17))
    wide_wrap = max(600, int(w * 0.55))

    def styleConfig(backgroundColor: str, fieldBackgroundColor: str, accent1: str, accent2: str, fontF: str, fontS: str):
        style = ttk.Style(root)
        root.configure(bg=backgroundColor)
        canvas.configure(background=backgroundColor)

        style.configure(
            "TFrame",
            foreground=accent1,
            background=backgroundColor,
            padding=20,
            font=(fontF, fontS),
        )
        style.configure(
            "TButton",
            foreground=accent1,
            background=backgroundColor,
            borderwidth=2,
            bordercolor=accent2,
            font=(fontF, fontS),
        )
        style.map(
            "TButton",
            foreground=[("pressed", "#2F274D"), ("active", "blue")],
            fieldbackground=[("active", "#947AFB")],
            background=[("active", "#947AFB")],
            relief=[("pressed", "sunken")],
        )
        style.configure(
            "TLabel",
            background=backgroundColor,
            foreground=accent1,
            padding=10,
            font=(fontF, fontS),
        )
        style.configure(
            "TEntry",
            background=backgroundColor,
            borderwidth=2,
            bordercolor=accent2,
            foreground=accent1,
            relief="flat",
            font=(fontF, fontS),
        )

    def set_light():
        styleConfig(l_bg_color, l_field_bg_color, l_accent1, l_accent2, fontF, fontS)

    def set_dark():
        styleConfig(d_bg_color, d_field_bg_color, d_accent1, d_accent2, fontF, fontS)

    styleConfig(l_bg_color, l_field_bg_color, l_accent1, l_accent2, fontF, fontS)

    def section(title: str, fSize: float = 1.5, colSpan: int = 2, columnOffset: int = 0, rowOffset: int = 0):
        nonlocal row
        ttk.Label(
            scroll_frame,
            text=title,
            font=(fontF, int(fontS * fSize), "bold"),
        ).grid(row=row + rowOffset, column=0 + columnOffset, columnspan=colSpan, sticky="w", pady=(10, 2))
        row += 1

    def special_section(title: str, fSize: float = 1.5, fColor: str = l_accent1, bgColor: str = l_bg_color,
                        colSpan: int = 2, columnOffset: int = 0, rowOffset: int = 0):
        nonlocal row
        tk.Label(
            scroll_frame,
            text=title,
            font=(fontF, int(fontS * fSize), "bold"),
            fg=fColor,
            bg=bgColor,
            padx=12,
            pady=6,
        ).grid(row=row + rowOffset, column=0 + columnOffset, columnspan=colSpan, sticky="w", pady=(10, 2))
        row += 1

    def stat(label: str, value, fSize: float = 1):
        nonlocal row
        ttk.Label(scroll_frame, text=label, font=(fontF, int(fontS * fSize))).grid(row=row, column=0, sticky="w")
        ttk.Label(scroll_frame, text=str(value), font=(fontF, int(fontS * fSize))).grid(row=row, column=1, sticky="w")
        row += 1

    def wrapped_value_label(r: int, c: int, value: str, fSize: float = 0.7):
        ttk.Label(
            scroll_frame,
            text=value,
            font=(fontF, int(fontS * fSize)),
            wraplength=value_wrap,
            justify="left",
        ).grid(row=r, column=c, sticky="w")

    def top_list(title: str, items, last: int, column: int = 0):
        nonlocal row
        nCol = column * 2
        mCol = 4
        if column > 0:
            row = row - mCol

        ttk.Label(scroll_frame, text=title, font=(fontF, int(fontS * 1), "bold")).grid(
            row=row, column=0 + nCol, sticky="w", pady=(10, 2)
        )
        row += 1

        actual_items = list(items[:last]) if items else []
        for i in range(last):
            label = f"{i+1}th Place:"
            value = clean_item(actual_items[i]) if i < len(actual_items) else "-"
            ttk.Label(scroll_frame, text=label, font=(fontF, int(fontS * 0.7))).grid(row=row, column=0 + nCol, sticky="w")
            wrapped_value_label(row, 1 + nCol, value, 0.7)
            row += 1

    def progress_bar(label: str, value: float | int):
        nonlocal row
        ttk.Label(scroll_frame, text=label).grid(row=row, column=0, sticky="w")
        ttk.Progressbar(scroll_frame, value=float(value), length=200, mode="determinate").grid(row=row, column=1, sticky="w")
        ttk.Label(scroll_frame, text=f" {float(value):.1f}%").grid(row=row, column=2, sticky="w")
        row += 1

    def bullet_lines(title: str, items: list[str], fSize: float = 0.65):
        nonlocal row
        section(title, 1.2, 6)
        if not items:
            stat(" None", "-")
            return
        for line in items:
            ttk.Label(
                scroll_frame,
                text=f"• {line}",
                font=(fontF, int(fontS * fSize)),
                wraplength=wide_wrap,
                justify="left",
            ).grid(row=row, column=0, columnspan=6, sticky="w")
            row += 1

    def recommendation_cards(title: str, items: list[dict], max_items: int = 5):
        nonlocal row
        section(title, 1.5, 6)
        if not items:
            stat(" Recommendations", "None yet")
            return

        for idx, rec in enumerate(items[:max_items], start=1):
            ttk.Label(
                scroll_frame,
                text=f"{idx}. {rec.get('title', '')}",
                font=(fontF, int(fontS * 0.9), "bold"),
                wraplength=wide_wrap,
                justify="left",
            ).grid(row=row, column=0, columnspan=6, sticky="w")
            row += 1
            ttk.Label(
                scroll_frame,
                text=f"Channel: {rec.get('channel', '')}   |   Category: {clean_item(rec.get('category', ''))}   |   Score: {rec.get('score', '')}",
                font=(fontF, int(fontS * 0.65)),
                wraplength=wide_wrap,
                justify="left",
            ).grid(row=row, column=0, columnspan=6, sticky="w")
            row += 1
            ttk.Label(
                scroll_frame,
                text=rec.get("url", ""),
                font=(fontF, int(fontS * 0.60)),
                wraplength=wide_wrap,
                justify="left",
            ).grid(row=row, column=0, columnspan=6, sticky="w")
            row += 1

    section("AI Network IDS", 1.8, 3)
    ttk.Button(scroll_frame, text="☾⋆", command=set_dark).grid(row=0, column=4)
    ttk.Button(scroll_frame, text="☀︎", command=set_light).grid(row=0, column=5)

    section("The provided network data is:", 1.5)
    section("Benign", 1)

    commentOut = '''
    totals = stats["totals"]
    section("Totals", 1.5)
    stat(" Total Watch sessions", totals["total_watch_events"], 1)
    stat(" Unique Videos", totals["unique_videos"], 1)
    stat(" Shorts Count", totals["shorts_count"], 1)
    progress_bar(" Shorts Percent", totals["shorts_percent"])
    if float(totals["shorts_percent"]) > 70:
        section("You got a problem (ŏ_ŏ˘)", 1, 2, 2, -2)

    section("Top most viewed", 1.5)
    top_list("Top Categories", stats.get("top_categories", []), 3, 0)
    top_list("Top Channels", stats.get("top_channels", []), 3, 1)
    top_list("Top Tags", stats.get("top_tags", []), 3, 2)
    top_list("Top Hashtags", stats.get("top_hashtags", []), 3, 0)
    top_list("Top Topic Categories", stats.get("top_topic_categories", []), 3, 1)

    duration = stats["duration"]
    section("Time Stats!", 1.5)
    stat(" Total seconds viewed:", duration["total_seconds"], 0.8)
    stat(" Average video duration:", duration["average_seconds"], 0.8)
    stat(" Longest video lenght:", duration["max_seconds"], 0.8)
    stat(" Shortest video lenght:", duration["min_seconds"], 0.8)

    section("Video length counter", 1)
    buckets = duration["buckets"]
    stat(" Videos from 0 to 60 seconds:", buckets["0_60s"], 0.8)
    stat(" Videos from 1 to 5 minutes:", buckets["61s_5m"], 0.8)
    stat(" Videos from 5 to 20 minutes:", buckets["5m_20m"], 0.8)
    stat(" Videos of 20 minutes or more:", buckets["20m_plus"], 0.8)

    section("Lat's talk Schedule!!", 1.5)
    tPatterns = stats.get("time_patterns", {})
    top_hours = tPatterns.get("top_hours", [])
    top_list("Top Viewing hours", top_hours, 3, 0)

    strongest_hour = None
    if top_hours:
        first = top_hours[0]
        try:
            strongest_hour = int(first[0] if isinstance(first, (list, tuple)) else first)
        except Exception:
            strongest_hour = None

    if strongest_hour is not None and strongest_hour < 3:
        special_section("You are a Nocturnal Creature ₍^. .^₎⟆ ", 1.5, "#ecebc9", "#1A1A1A", 3, 2, -4)
    elif strongest_hour is not None and strongest_hour > 20:
        special_section("What a functional member of society!!", 1.5, "#FFFFFF", "#5189BA")

    content_profile = ai_features.get("content_profile", {})
    section("AI Profile", 1.5)
    stat(" Prefers Shorts", content_profile.get("prefers_shorts", False), 0.8)
    bullet_lines("AI Insights", [str(x) for x in ai_insights], 0.7)
    bullet_lines("Topic Clusters", [clean_item(x) for x in topic_clusters], 0.68)
    recommendation_cards("Recommended videos for you", recommendations, 5)
    bullet_lines("Output Files", [str(x) for x in output_files], 0.62)
    '''

    root.mainloop()



def main():
    output_dict = {
            "stats": {
                "totals": {
                    "total_watch_events": 10,
                    "unique_videos": 8,
                    "shorts_count": 3,
                    "shorts_percent": 30.0
                },
                "top_categories": ["Cat1", "Cat2", "Cat3"],
                "top_channels": ["Chan1", "Chan2", "Chan3"],
                "top_tags": ["Tag1", "Tag2", "Tag3"],
                "top_hashtags": ["Hash1", "Hash2", "Hash3"],
                "top_topic_categories": ["Topic1", "Topic2", "Topic3"],
                "duration": {
                    "total_seconds": 1000,
                    "average_seconds": 100,
                    "median_seconds": 90,
                    "max_seconds": 300,
                    "min_seconds": 10,
                    "buckets": {
                        "0_60s": 1,
                        "61s_5m": 5,
                        "5m_20m": 3,
                        "20m_plus": 1
                    }
                },
                "time_patterns": {
                    "top_hours": [10, 15, 20]
                }
            }
    }

    show_results(output_dict)


if __name__ == "__main__":
    main()