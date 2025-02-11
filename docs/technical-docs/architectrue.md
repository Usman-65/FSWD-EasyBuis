---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
[Jane Dane]

{: .no_toc }
# Architecture

    Diese Seite beschreibt die Struktur der Anwendung und wie wichtige Teile der App funktionieren. Sie soll neuen Entwicklern ausreichend technisches Wissen vermitteln, um zum Code beitragen zu können.

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Übersicht

EasyBuis Task Manager ist eine Webanwendung zur Verwaltung von Aufgaben und Workflows mithilfe eines Kanban-Systems. Die Anwendung ermöglicht es Benutzern, Aufgaben zu erstellen, zu aktualisieren, zu verschieben und zu löschen, wobei rollenbasierte Zugriffskontrollen durchgesetzt werden. Sie basiert auf Flask, SQLite sowie einer Kombination aus HTML, CSS und JavaScript und bietet eine intuitive Benutzeroberfläche für eine effiziente Aufgabenverwaltung.

## Codemap

Das Projekt folgt einer modularen Struktur mit wichtigen Komponenten, die in verschiedenen Dateien organisiert sind:

app.py: Der Haupteinstiegspunkt der Anwendung. Initialisiert die Flask-App, die Datenbank und registriert Blueprints.

auth_utils.py: Implementiert die rollenbasierte Zugriffskontrolle mittels Dekoratoren.

kanban_board.py: Verwaltet die Funktionen des Kanban-Boards, einschließlich Aufgabenverschiebung und -anzeige.

Task_Manager.py: Verantwortlich für CRUD-Operationen für Aufgaben und Checklisten.

templates/: Enthält HTML-Templates für die Darstellung der Ansichten.

static/: Speichert CSS-Stylesheets und JavaScript-Dateien zur Verbesserung der Benutzeroberfläche.

nutzer.db: SQLite-Datenbank zur Speicherung von Benutzern, Aufgaben und Checklisten.

## Systemübersicht

Die Anwendung folgt einer modularen Architektur mit einer klaren Trennung der Verantwortlichkeiten. Die wichtigsten Komponenten sind:

Frontend: HTML, CSS (Bootstrap), JavaScript für die Benutzeroberfläche.

Backend: Flask als Webframework für die Serverlogik.

Datenbank: SQLite zur Speicherung von Benutzer-, Aufgaben- und Berechtigungsdaten.

Authentifizierung: Sitzungsgesteuerte Anmeldung mit rollenbasiertem Zugriff.

## Hauptkomponenten

1. Flask Backend

Das Backend ist in Python mit Flask implementiert und stellt Endpunkte zur Verwaltung von Aufgaben und Benutzern bereit.

app.py: Startpunkt der Anwendung, Initialisierung von Flask und Registrierung der Blueprints.

auth_utils.py: Implementiert rollenbasierte Zugriffskontrolle.

kanban_board.py: Verwaltung von Aufgaben und Kanban-Logik.

Task_Manager.py: CRUD-Operationen  (Create, Read, Update, Delete) für Aufgaben.

2. Datenbank

SQLite wird zur Speicherung aller relevanten Daten verwendet. Die wichtigsten Tabellen sind:

users: Speichert Benutzerinformationen und Rollen.

tasks: Enthält Aufgabeninformationen mit Status (To Do, In Progress, Done).

checklist: Zusätzliche Punkte innerhalb von Aufgaben.

3. Benutzeroberfläche

Bootstrap für Styling und responsives Design.

Dynamische Updates durch JavaScript zur Interaktion mit dem Kanban-Board.

## Modularisierung durch Blueprints

kanban_board und task_manager sind separate Flask-Blueprints, um eine klare Trennung der Verantwortlichkeiten zu gewährleisten.


## Sicherheitsaspekte

Die Anwendung verwendet verschiedene Sicherheitsmechanismen:

Passwortverschlüsselung mit werkzeug.security.

Sitzungsbasierte Authentifizierung für Benutzerverwaltung.

Rollenbasierte Zugriffskontrolle (RBAC) zur Einschränkung von Funktionen basierend auf Benutzerrollen.


## Skalierbarkeit und Deployment

Die Anwendung kann mit geringem Aufwand auf Cloud-Umgebungen wie AWS oder Heroku bereitgestellt werden.

Skalierungsmöglichkeiten bestehen durch die Migration auf eine leistungsfähigere Datenbank wie PostgreSQL.

Falls in Zukunft eine API-Anbindung erforderlich wird, kann Flask’s RESTful-Unterstützung genutzt werden.

Es besteht die Möglichkeit zur Implementierung von Webhooks oder externer Datenanbindung zur Automatisierung von Workflows.


Weitere Details sind unter design decisions zu finden
