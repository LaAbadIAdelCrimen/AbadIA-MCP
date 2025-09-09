# Agent Strategies

This file contains a list of high-level strategies that the planner agent can use to make decisions.

## Core Monastic Duties
*   `attend_prayer`: Go to the church for the current prayer service.
*   `go_to_meal`: Go to the refectory for the midday or evening meal.
*   `return_to_cell`: Return to William's and Adso's cell, especially at night.

## Investigation
*   `investigate_crime_scene`: Go to the location of the most recent murder and search for clues.
*   `investigate_library`: Go to the library to search for books and clues.
*   `investigate_scriptorium`: Go to the scriptorium to investigate the monks' work.
*   `investigate_infirmary`: Go to the infirmary to investigate medical supplies and records.

## Social Interaction
*   `follow_character`: Follow a specific character to observe their behavior (e.g., `follow_abbot`, `follow_jorge`).
*   `talk_to_character`: Approach and talk to a specific character (e.g., `talk_to_severinus`).

## Exploration
*   `explore_location`: Explore a specific location to map it out and find items (e.g., `explore_church`, `explore_stables`).
*   `explore_abbey_randomly`: Wander the abbey to see if anything new has appeared.

## Object Interaction
*   `get_object`: Pick up a specific object (e.g., `get_key`, `get_book`).
*   `use_object`: Use an object from the inventory (e.g., `use_key`).