"""
stepdistance.visualization
==========================

Matplotlib-based chart generators for route calculation results.

Charts
------
* **Bar chart** — steps per segment.
* **Pie chart** — percentage contribution of each segment to total distance.
* **Line chart** — cumulative steps across segments.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

from stepdistance.calculator import RouteResult

logger = logging.getLogger(__name__)


def _ensure_matplotlib():
    """Lazily import and return ``matplotlib.pyplot``.

    Raises
    ------
    ImportError
        If matplotlib is not installed.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")  # Non-interactive backend for file output
        import matplotlib.pyplot as plt
        return plt
    except ImportError as exc:
        raise ImportError(
            "Visualization requires 'matplotlib'.  "
            "Install it with:  pip install matplotlib"
        ) from exc


# ---------------------------------------------------------------------------
# Bar chart — steps per segment
# ---------------------------------------------------------------------------


def plot_steps_bar(
    result: RouteResult,
    save_path: Optional[str] = None,
    *,
    show: bool = False,
) -> Optional[str]:
    """Generate a bar chart of steps for each route segment.

    Parameters
    ----------
    result:
        A :class:`RouteResult` with segment data.
    save_path:
        If provided, the chart is saved to this file path.
    show:
        If ``True``, display the chart in an interactive window.

    Returns
    -------
    str or None
        Absolute path of saved image, or ``None`` if not saved.
    """
    plt = _ensure_matplotlib()

    labels = [sr.origin + " -> " + sr.destination for sr in result.segment_results]
    steps = [sr.steps_rounded for sr in result.segment_results]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Gradient-like colour palette
    colors = plt.cm.viridis([i / max(len(labels) - 1, 1) for i in range(len(labels))])

    bars = ax.bar(labels, steps, color=colors, edgecolor="white", linewidth=0.8)
    ax.set_xlabel("Route Segment", fontsize=12)
    ax.set_ylabel("Steps", fontsize=12)
    ax.set_title(f"Steps per Segment — {result.person.name}", fontsize=14, fontweight="bold")
    ax.tick_params(axis="x", rotation=25)

    # Annotate bar tops
    for bar, val in zip(bars, steps):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{val:,}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    fig.tight_layout()
    saved = _save(fig, save_path)
    if show:
        plt.show()
    plt.close(fig)
    return saved


# ---------------------------------------------------------------------------
# Pie chart — distance contribution
# ---------------------------------------------------------------------------


def plot_distance_pie(
    result: RouteResult,
    save_path: Optional[str] = None,
    *,
    show: bool = False,
) -> Optional[str]:
    """Generate a pie chart of each segment's distance contribution.

    Parameters
    ----------
    result:
        A :class:`RouteResult` with segment data.
    save_path:
        If provided, the chart is saved to this file path.
    show:
        If ``True``, display the chart interactively.

    Returns
    -------
    str or None
        Absolute path of saved image, or ``None`` if not saved.
    """
    plt = _ensure_matplotlib()

    labels = [p["label"] for p in result.percentages]
    sizes = [p["percentage"] for p in result.percentages]

    colors = plt.cm.Set2([i / max(len(labels) - 1, 1) for i in range(len(labels))])

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        textprops={"fontsize": 10},
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
    ax.set_title(
        f"Distance Contribution — {result.person.name}",
        fontsize=14,
        fontweight="bold",
        pad=20,
    )

    fig.tight_layout()
    saved = _save(fig, save_path)
    if show:
        plt.show()
    plt.close(fig)
    return saved


# ---------------------------------------------------------------------------
# Line chart — cumulative steps
# ---------------------------------------------------------------------------


def plot_cumulative_line(
    result: RouteResult,
    save_path: Optional[str] = None,
    *,
    show: bool = False,
) -> Optional[str]:
    """Generate a line chart of cumulative steps across segments.

    Parameters
    ----------
    result:
        A :class:`RouteResult` with segment data.
    save_path:
        If provided, the chart is saved to this file path.
    show:
        If ``True``, display the chart interactively.

    Returns
    -------
    str or None
        Absolute path of saved image, or ``None`` if not saved.
    """
    plt = _ensure_matplotlib()

    # Build x-axis labels (destination cities, starting with origin of first)
    x_labels = [result.segment_results[0].origin]
    for sr in result.segment_results:
        x_labels.append(sr.destination)

    # y-values: 0 at origin, then cumulative steps
    y_values = [0] + result.cumulative_steps

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        x_labels,
        y_values,
        marker="o",
        markersize=8,
        linewidth=2.5,
        color="#4A90D9",
        markerfacecolor="#E94E77",
        markeredgecolor="white",
        markeredgewidth=1.5,
    )

    # Annotate points
    for x, y in zip(x_labels, y_values):
        ax.annotate(
            f"{y:,}",
            (x, y),
            textcoords="offset points",
            xytext=(0, 12),
            ha="center",
            fontsize=9,
        )

    ax.set_xlabel("Location", fontsize=12)
    ax.set_ylabel("Cumulative Steps", fontsize=12)
    ax.set_title(
        f"Cumulative Steps — {result.person.name}",
        fontsize=14,
        fontweight="bold",
    )
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    saved = _save(fig, save_path)
    if show:
        plt.show()
    plt.close(fig)
    return saved


# ---------------------------------------------------------------------------
# Generate all charts
# ---------------------------------------------------------------------------


def plot_all(
    result: RouteResult,
    save_dir: Optional[str] = None,
    *,
    show: bool = False,
) -> list[str]:
    """Generate all three chart types and optionally save them.

    Parameters
    ----------
    result:
        A :class:`RouteResult` with segment data.
    save_dir:
        Directory to save charts into.  Files are named
        ``steps_bar.png``, ``distance_pie.png``, ``cumulative_line.png``.
    show:
        If ``True``, display each chart interactively.

    Returns
    -------
    list[str]
        Absolute paths of saved chart images (empty if *save_dir* is
        ``None``).
    """
    paths: list[str] = []

    bar_path = os.path.join(save_dir, "steps_bar.png") if save_dir else None
    pie_path = os.path.join(save_dir, "distance_pie.png") if save_dir else None
    line_path = os.path.join(save_dir, "cumulative_line.png") if save_dir else None

    p = plot_steps_bar(result, save_path=bar_path, show=show)
    if p:
        paths.append(p)

    p = plot_distance_pie(result, save_path=pie_path, show=show)
    if p:
        paths.append(p)

    p = plot_cumulative_line(result, save_path=line_path, show=show)
    if p:
        paths.append(p)

    return paths


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------


def _save(fig, path: Optional[str]) -> Optional[str]:
    """Save a figure if a path is provided.

    Parameters
    ----------
    fig:
        Matplotlib figure object.
    path:
        Destination file path.

    Returns
    -------
    str or None
        Absolute path if saved, else ``None``.
    """
    if path is None:
        return None
    abs_path = os.path.abspath(path)
    os.makedirs(os.path.dirname(abs_path) or ".", exist_ok=True)
    fig.savefig(abs_path, dpi=150, bbox_inches="tight")
    logger.info("Chart saved to %s", abs_path)
    return abs_path
