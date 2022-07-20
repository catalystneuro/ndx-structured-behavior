"""
Module with helper functions for plotting the behavioral data tables defined in the ndx_beadl extension
"""
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
from typing import Union
from ndx_beadl import (EventsTable, EventTypesTable,
                       ActionTable, ActionTypesTable,
                       StatesTable, StateTypesTable,
                       TrialsTable)


def plot_events(events: Union[EventsTable, pd.DataFrame],
                event_types: EventTypesTable,
                show_event_values: bool = True,
                marker: str = None,
                figsize: tuple = None,
                fontsize: int = 18,
                marker_size: int = None,
                marker_width: int = None,
                marker_color=None,
                y_offset: float = 0,
                keep_yticks: bool = False,
                fig=None):
    """
    Plot a tick plot showing the times of events.

    :param events: The EventsTable or a DataFrame from subsetting the EventsTable, e.g., via events[0:100]
    :param event_types: The EventTypesTable that corresponds to EventsTable
    :param show_event_values: Separate events both by type and value (True) or by type only (False). (Default=True)
    :param marker: String marker to use in scatter plot. (Default="|")
    :param figsize: Figure size tuple
    :param fontsize: Fontsize (Default=18)
    :param y_offset: Offset in the y axis to use. This is used to shift the plot when combining multiple
                     plots, e.g., an events and actions plot, in the same figure.
    :param keep_yticks: When combining with other plots (e.g,. events, actions, or states), we may want to
                     keep the text and location of existing ytick lables. (Default=False)
    :param fig: Matplotlib figure. If None then create a new figure, otherwise assume that a figure exists.
                (Default=None, i.e., create a new figure)

    :return: Matplotlib figure. Call plt.show() to render the figure.
    """
    edf = events if isinstance(events, pd.DataFrame) else events.to_dataframe(index=True)
    x_values = edf['timestamp'][:]
    # show events by type and value
    if show_event_values:
        event_types_loaded = event_types['event_name'][:]
        events_and_values_merged = list(zip([event_types_loaded[i] for i in edf['event_type'][:]], edf['value'][:]))
        event_types_and_values = list(set(events_and_values_merged))
        y_values = [event_types_and_values.index(ev) + y_offset for ev in events_and_values_merged]
        y_tick_labels = ["%s(%s)" % v for v in event_types_and_values]
        y_label = "Event type"
    # Show events by type
    else:
        y_values = np.asarray(edf['event_type'][:]) + y_offset
        y_tick_labels = event_types['event_name'][:]
        y_label = "Event type"
    if fig is None:
        fig = plt.figure(figsize=(18, 3) if figsize is None else figsize)
    plt.scatter(
        x_values,
        y_values,
        marker='|' if marker is None else marker,
        s=marker_size,
        linewidth=marker_width,
        color=marker_color)
    plt.xlabel('Time in seconds (s)', fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    if keep_yticks:
        tp = plt.yticks()[0].tolist()
        tl = [t.get_text() for t in plt.yticks()[1]]
        plt.yticks(np.arange(y_offset, y_offset + len(y_tick_labels)).tolist() + tp,
                   y_tick_labels + tl,
                   fontsize=fontsize)
    else:
        plt.yticks(np.arange(np.min(y_values), np.max(y_values) + 1), y_tick_labels, fontsize=fontsize)
    plt.ylabel(y_label, fontsize=fontsize)
    return fig


def plot_actions(actions: Union[ActionTable, pd.DataFrame],
                 action_types: ActionTypesTable,
                 show_action_values: bool = True,
                 marker: str = None,
                 figsize: tuple = None,
                 fontsize: int = 18,
                 marker_size: int = None,
                 marker_width: int = None,
                 marker_color=None,
                 y_offset: float = 0,
                 keep_yticks: bool = False,
                 fig=None):
    """
    Plot a tick plot showing the times of actions.

    :param actions: The ActionTable or a DataFrame from subsetting the ActionTable, e.g., via actions[0:100]
    :param action_types: The ActionTypesTable that corresponds to ActionTable
    :param show_event_values: Separate events both by type and value (True) or by type only (False). (Default=True)
    :param marker: String marker to use in scatter plot. (Default="|")
    :param figsize: Figure size tuple
    :param fontsize: Fontsize (Default=18)
    :param y_offset: Offset in the y axis to use. This is used to shift the plot when combining multiple
                     plots, e.g., an events and actions plot, in the same figure.
    :param keep_yticks: When combining with other plots (e.g,. events, actions, or states), we may want to
                     keep the text and location of existing ytick lables. (Default=False)
    :param fig: Matplotlib figure. If None then create a new figure, otherwise assume that a figure exists.
                (Default=None, i.e., create a new figure)

    :return: Matplotlib figure. Call plt.show() to render the figure.
    """
    adf = actions if isinstance(actions, pd.DataFrame) else actions.to_dataframe(index=True)
    x_values = adf['action_time'][:]
    # show events by type and value
    if show_action_values:
        action_types_loaded = action_types['action_name'][:]
        actions_and_values_merged = list(zip([action_types_loaded[i] for i in adf['action_type'][:]], adf['value'][:]))
        action_types_and_values = list(set(actions_and_values_merged))
        y_values = [action_types_and_values.index(av) + y_offset for av in actions_and_values_merged]
        y_tick_labels = ["%s(%s)" % v for v in action_types_and_values]
        y_label = "Action type"
    # Show events by type
    else:
        y_values = np.asarray(adf['action_type'][:]) + y_offset
        y_tick_labels = action_types['action_name'][:]
        y_label = "Action type"
    if fig is None:
        fig = plt.figure(figsize=(18, 3) if figsize is None else figsize)
    plt.scatter(x_values,
                y_values,
                marker='|' if marker is None else marker,
                s=marker_size,
                linewidth=marker_width,
                color=marker_color)
    plt.xlabel('Time in seconds (s)', fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    if keep_yticks:
        tp = plt.yticks()[0].tolist()
        tl = [t.get_text() for t in plt.yticks()[1]]
        plt.yticks(np.arange(y_offset, y_offset + len(y_tick_labels)).tolist() + tp,
                   y_tick_labels + tl,
                   fontsize=fontsize)
    else:
        plt.yticks(np.arange(np.min(y_values), np.max(y_values) + 1), y_tick_labels, fontsize=fontsize)
        plt.ylabel(y_label, fontsize=fontsize)
    return fig


def plot_states(states: Union[StatesTable, pd.DataFrame],
                state_types: StateTypesTable,
                figsize: tuple = None,
                fontsize: int = 18,
                rectangle_height: float = 1,
                rectangle_color=None,
                show_instantenous_states_markers: bool = True,
                marker_color="red",
                marker: str = "|",
                marker_width: int = 1,
                marker_size: int = None,
                y_offset: float = 0,
                keep_yticks: bool = False,
                fig=None):
    """
    Plot time ranges for states.

    Some states may have the same start_time and stop_time, and are, hence, instantaneous.
    Such states will normally not show up in the plot, as the corresponding rectangle would
    have a width of 0. To show those states as well, they can be plotted separately as a scatter
    plot.


    :param states: The StatesTable or a DataFrame from subsetting the StatesTable, e.g., via actions[0:100]
    :param state_types: The StateTypesTable that corresponds to StatesTable
    :param figsize: Figure size tuple
    :param fontsize: Fontsize (Default=18)
    :param rectangle_height: Height of the rectangles along the y-axis. This should normally be
                             between 0 and 1. (Default=1)
    :param show_instantenous_states_markers: Show states with a duration of 0 separately via
                             scatter plot markers (Default=True)
    :param marker_color: Color for scatter plot markers for instantenous states. (Default=red)
    :param marker: Maker string for scatter plot markers for instantenous states. (Default="|")
    :param marker_width: Linewidth for scatter plot markers for instantenous states. (Default=1)
    :param marker_size: Height size for scatter plot markers for instantenous states. (Default=1000):
    :param y_offset: Offset in the y axis to use. This is used to shift the plot when combining multiple
                     plots, e.g., an events and actions plot, in the same figure.
    :param keep_yticks: When combining with other plots (e.g,. events, actions, or states), we may want to
                     keep the text and location of existing ytick lables. (Default=False)
    :param fig: Matplotlib figure. If None then create a new figure, otherwise assume that a figure exists.
                (Default=None, i.e., create a new figure)

    :return: Matplotlib figure. Call plt.show() to render the figure.
    """
    sdf = states if isinstance(states, pd.DataFrame) else states.to_dataframe(index=True)
    x_start = sdf['start_time'][:].to_numpy()
    x_stop = sdf['stop_time'][:]
    x_range = np.asarray([xs[1] - xs[0] for xs in zip(x_start, x_stop)])

    y_height = rectangle_height
    y_values = np.asarray(sdf['state_type'][:]) - (y_height * 0.5) + y_offset
    y_tick_labels = state_types['state_name'][:]
    y_label = "State type"

    patches = [mpl.patches.Rectangle((x_start[i], y_values[i]), x_range[i], y_height, color=rectangle_color)
               for i in range(len(x_start))]

    if fig is None:
        fig, ax = plt.subplots(figsize=(18, 3) if figsize is None else figsize)
    else:
        ax = plt.gca()
    ax.add_collection(mpl.collections.PatchCollection(patches, color=rectangle_color))

    if show_instantenous_states_markers:
        instantaneous_events = x_range == 0
        if np.sum(instantaneous_events) > 0:
            plt.scatter(x_start[instantaneous_events],
                        y_values[instantaneous_events] + y_height * 0.5,
                        marker=marker,
                        color=marker_color,
                        s=marker_size,
                        linewidth=marker_width)

    plt.xlabel('Time in seconds (s)', fontsize=fontsize)
    plt.xlim(np.min(x_start), np.max(x_stop))
    plt.ylim(np.min(y_values), np.max(y_values) + 1)
    plt.xticks(fontsize=fontsize)
    if keep_yticks:
        tp = plt.yticks()[0].tolist()
        tl = [t.get_text() for t in plt.yticks()[1]]
        plt.yticks(np.arange(y_offset, y_offset + len(y_tick_labels)).tolist() + tp,
                   y_tick_labels + tl,
                   fontsize=fontsize)
    else:
        plt.yticks(np.arange(y_offset, y_offset + len(y_tick_labels)).tolist(),
                   y_tick_labels,
                   fontsize=fontsize)
        plt.ylabel(y_label, fontsize=fontsize)
    plt.ylabel(y_label, fontsize=fontsize)
    return fig


def plot_trials(trials: Union[TrialsTable, pd.DataFrame],
                states: StatesTable,
                state_types: StateTypesTable,
                actions: ActionTable,
                action_types: ActionTypesTable,
                events: EventsTable,
                event_types: EventTypesTable,
                figsize=None,
                fontsize=18,
                rectangle_height=1,
                marker_size=None):
    """
   Plot the event, actions, states, and trial times for one or more trials

   :param trials: The TrialsTable or a DataFrame from subsetting the TrialsTable, e.g., via trials[0:100]
   :param states: The StatesTable
   :param state_types: The StateTypesTable that corresponds to StatesTable
   :param actions: The ActionTable
   :param action_types: The ActionTypesTable that corresponds to ActionTable
   :param events: The EventsTable
   :param event_types: The EventTypesTable that corresponds to EventsTable
   :param show_event_values: Separate events both by type and value (True) or by type only (False). (Default=True)
   :param marker: String marker to use in scatter plot. (Default="|")
   :param figsize: Figure size tuple (Default=(18,10))
   :param fontsize: Fontsize (Default=18)
   :param rectangle_height: Height of the rectangles along the y-axis. This should normally be
                             between 0 and 1. (Default=1)
   :param marker_size: Height size for scatter plot markers for instantaneous acions/events/tates. (Default=None):

   :return: Matplotlib figure. Call plt.show() to render the figure.
    """

    trials_df = trials if isinstance(trials, pd.DataFrame) else trials.to_dataframe(index=True)
    fig = plt.figure(figsize=(18, 10) if figsize is None else figsize)
    events_index = [j for i in trials_df["events"] for j in i]
    plot_events(events=events[events_index],
                event_types=event_types,
                show_event_values=True,
                marker_size=marker_size,
                marker_width=2,
                marker_color='blue',
                y_offset=0,
                fontsize=fontsize,
                fig=fig)
    actions_index = [j for i in trials_df["actions"] for j in i]
    y_offset = np.ceil(plt.ylim()[1])
    if y_offset == plt.ylim()[1]:
        y_offset += 1
    plot_actions(actions=actions[actions_index],
                 action_types=action_types,
                 show_action_values=True,
                 marker_size=marker_size,
                 marker_width=2,
                 marker_color='green',
                 y_offset=y_offset,
                 keep_yticks=True,
                 fontsize=fontsize,
                 fig=fig)
    states_index = [j for i in trials_df["states"] for j in i]
    y_offset = np.ceil(plt.ylim()[1])
    if y_offset == plt.ylim()[1]:
        y_offset += 1
    plot_states(states=states[states_index],
                state_types=state_types,
                y_offset=y_offset,
                rectangle_height=1,
                rectangle_color='black',
                marker_color="red",
                marker_size=marker_size,
                keep_yticks=True,
                fontsize=fontsize,
                show_instantenous_states_markers=True,
                fig=fig)
    # Draw the trial start/end time boxes
    x_start = trials_df['start_time'][:].to_numpy()
    x_stop = trials_df['stop_time'][:]
    x_range = np.asarray([xs[1] - xs[0] for xs in zip(x_start, x_stop)])

    y_height = rectangle_height
    y_offset = -1
    y_values = np.zeros(len(trials_df)) + y_offset - (y_height * 0.5)
    patches = [mpl.patches.Rectangle((x_start[i], y_values[i]), x_range[i], y_height)
               for i in range(len(x_start))]
    ax = plt.gca()
    ax.add_collection(
        mpl.collections.PatchCollection(patches, color=['gray' if i % 2 else 'lightgray' for i in range(len(patches))]))
    for i, r in enumerate(patches):
        rx, ry = r.get_xy()
        cx = rx + r.get_width() / 2.0
        cy = ry + r.get_height() / 2.0
        ax.annotate(trials_df.index[i], (cx, cy), color='w',  # weight='bold',
                    fontsize=fontsize - 3, ha='center', va='center')
    plt.xticks(x_start)
    plt.ylabel("Event / Action / State")
    plt.ylim(-1.5, plt.ylim()[1])
    plt.grid(axis='x')
    secax = ax.secondary_xaxis('top')
    secax.set_xticks(x_stop)

    return fig