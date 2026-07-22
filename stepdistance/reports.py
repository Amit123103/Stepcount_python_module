"""
stepdistance.reports
====================

Report-generation utilities.

Supports:
    - Plain-text reports (console / file)
    - JSON export
    - CSV export
    - PDF export (via ``fpdf2``)
"""

from __future__ import annotations

import csv
import json
import logging
import os
from dataclasses import asdict
from io import StringIO
from typing import Optional

from stepdistance.calculator import RouteResult, StepResult

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates formatted reports from calculation results.

    Parameters
    ----------
    route_result:
        A :class:`RouteResult` produced by :class:`DistanceCalculator`.

    Examples
    --------
    >>> rg = ReportGenerator(route_result)
    >>> print(rg.generate_text())
    >>> rg.save_json("report.json")
    """

    def __init__(self, route_result: RouteResult) -> None:
        self.result = route_result

    # ------------------------------------------------------------------
    # Plain-text report
    # ------------------------------------------------------------------

    def generate_text(self) -> str:
        """Return a nicely formatted plain-text report.

        Returns
        -------
        str
            The complete text report ready for printing.
        """
        r = self.result
        lines: list[str] = []

        # Header
        lines.append("=" * 60)
        lines.append("         STEP DISTANCE CALCULATOR - REPORT")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"Person              : {r.person.name}")
        lines.append(f"Average Step Length  : {r.person.step_length:.2f} m")
        lines.append("")
        lines.append("-" * 60)
        lines.append("Route Breakdown")
        lines.append("-" * 60)

        # Segments
        for idx, sr in enumerate(r.segment_results):
            pct = r.percentages[idx]["percentage"] if idx < len(r.percentages) else 0
            lines.append("")
            lines.append(f"  {sr.origin} -> {sr.destination}")
            lines.append(f"    Distance       : {sr.distance_m / 1000:,.2f} km  ({sr.distance_m:,.0f} m)")
            lines.append(f"    Steps Required : {sr.steps_rounded:,}")
            lines.append(f"    Contribution   : {pct:.2f}%")
            lines.append(f"    Cumulative Dist: {r.cumulative_distances[idx] / 1000:,.2f} km")
            lines.append(f"    Cumulative Steps: {r.cumulative_steps[idx]:,}")

        # Totals
        lines.append("")
        lines.append("-" * 60)
        lines.append("Totals")
        lines.append("-" * 60)
        lines.append(f"  Total Distance   : {r.total_distance_m / 1000:,.2f} km  ({r.total_distance_m:,.0f} m)")
        lines.append(f"  Total Steps      : {r.total_steps:,}")
        lines.append("=" * 60)

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # JSON export
    # ------------------------------------------------------------------

    def _to_dict(self) -> dict:
        """Convert the route result into a JSON-serialisable dictionary.

        Returns
        -------
        dict
            Serialisable representation of the result.
        """
        r = self.result
        return {
            "person": {
                "name": r.person.name,
                "gender": r.person.gender,
                "step_length_m": r.person.step_length,
            },
            "segments": [
                {
                    "origin": sr.origin,
                    "destination": sr.destination,
                    "distance_m": sr.distance_m,
                    "steps_exact": round(sr.steps_exact, 4),
                    "steps_rounded": sr.steps_rounded,
                    "percentage": r.percentages[i]["percentage"]
                    if i < len(r.percentages)
                    else 0,
                    "cumulative_distance_m": r.cumulative_distances[i],
                    "cumulative_steps": r.cumulative_steps[i],
                }
                for i, sr in enumerate(r.segment_results)
            ],
            "totals": {
                "total_distance_m": r.total_distance_m,
                "total_distance_km": round(r.total_distance_m / 1000, 2),
                "total_steps": r.total_steps,
            },
        }

    def save_json(self, filepath: str) -> str:
        """Save the report as a JSON file.

        Parameters
        ----------
        filepath:
            Destination file path.

        Returns
        -------
        str
            Absolute path of the written file.
        """
        data = self._to_dict()
        abs_path = os.path.abspath(filepath)
        os.makedirs(os.path.dirname(abs_path) or ".", exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
        logger.info("JSON report saved to %s", abs_path)
        return abs_path

    # ------------------------------------------------------------------
    # CSV export
    # ------------------------------------------------------------------

    def save_csv(self, filepath: str) -> str:
        """Save the report as a CSV file.

        Each row represents one route segment.

        Parameters
        ----------
        filepath:
            Destination file path.

        Returns
        -------
        str
            Absolute path of the written file.
        """
        abs_path = os.path.abspath(filepath)
        os.makedirs(os.path.dirname(abs_path) or ".", exist_ok=True)

        fieldnames = [
            "Origin",
            "Destination",
            "Distance_m",
            "Distance_km",
            "Steps_Exact",
            "Steps_Rounded",
            "Percentage",
            "Cumulative_Distance_m",
            "Cumulative_Steps",
        ]

        r = self.result
        with open(abs_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            for i, sr in enumerate(r.segment_results):
                writer.writerow(
                    {
                        "Origin": sr.origin,
                        "Destination": sr.destination,
                        "Distance_m": round(sr.distance_m, 2),
                        "Distance_km": round(sr.distance_m / 1000, 2),
                        "Steps_Exact": round(sr.steps_exact, 4),
                        "Steps_Rounded": sr.steps_rounded,
                        "Percentage": r.percentages[i]["percentage"]
                        if i < len(r.percentages)
                        else 0,
                        "Cumulative_Distance_m": round(r.cumulative_distances[i], 2),
                        "Cumulative_Steps": r.cumulative_steps[i],
                    }
                )
            # Totals row
            writer.writerow(
                {
                    "Origin": "TOTAL",
                    "Destination": "",
                    "Distance_m": round(r.total_distance_m, 2),
                    "Distance_km": round(r.total_distance_m / 1000, 2),
                    "Steps_Exact": "",
                    "Steps_Rounded": r.total_steps,
                    "Percentage": "100.00",
                    "Cumulative_Distance_m": round(r.total_distance_m, 2),
                    "Cumulative_Steps": r.total_steps,
                }
            )

        logger.info("CSV report saved to %s", abs_path)
        return abs_path

    # ------------------------------------------------------------------
    # PDF export
    # ------------------------------------------------------------------

    def save_pdf(self, filepath: str) -> str:
        """Save the report as a PDF file using ``fpdf2``.

        Parameters
        ----------
        filepath:
            Destination file path.

        Returns
        -------
        str
            Absolute path of the written file.

        Raises
        ------
        ImportError
            If ``fpdf2`` is not installed.
        """
        try:
            from fpdf import FPDF  # type: ignore[import-untyped]
        except ImportError as exc:
            raise ImportError(
                "PDF export requires the 'fpdf2' package.  "
                "Install it with:  pip install fpdf2"
            ) from exc

        r = self.result
        abs_path = os.path.abspath(filepath)
        os.makedirs(os.path.dirname(abs_path) or ".", exist_ok=True)

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Title
        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(0, 12, "Step Distance Calculator Report", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(6)

        # Person info
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(0, 8, f"Person: {r.person.name}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(
            0,
            8,
            f"Average Step Length: {r.person.step_length:.2f} m",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        pdf.ln(4)

        # Table header
        pdf.set_font("Helvetica", "B", 10)
        col_widths = [55, 55, 30, 30, 20]
        headers = ["Origin", "Destination", "Dist (km)", "Steps", "%"]
        for w, h in zip(col_widths, headers):
            pdf.cell(w, 8, h, border=1, align="C")
        pdf.ln()

        # Table rows
        pdf.set_font("Helvetica", "", 10)
        for i, sr in enumerate(r.segment_results):
            pct = r.percentages[i]["percentage"] if i < len(r.percentages) else 0
            pdf.cell(col_widths[0], 8, sr.origin, border=1)
            pdf.cell(col_widths[1], 8, sr.destination, border=1)
            pdf.cell(
                col_widths[2],
                8,
                f"{sr.distance_m / 1000:,.2f}",
                border=1,
                align="R",
            )
            pdf.cell(
                col_widths[3], 8, f"{sr.steps_rounded:,}", border=1, align="R"
            )
            pdf.cell(col_widths[4], 8, f"{pct:.1f}", border=1, align="R")
            pdf.ln()

        # Totals row
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(col_widths[0] + col_widths[1], 8, "TOTAL", border=1)
        pdf.cell(
            col_widths[2],
            8,
            f"{r.total_distance_m / 1000:,.2f}",
            border=1,
            align="R",
        )
        pdf.cell(col_widths[3], 8, f"{r.total_steps:,}", border=1, align="R")
        pdf.cell(col_widths[4], 8, "100.0", border=1, align="R")
        pdf.ln()

        pdf.output(abs_path)
        logger.info("PDF report saved to %s", abs_path)
        return abs_path
