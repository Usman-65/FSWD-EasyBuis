---
title: UI Components
nav_order: 99
---

{: .label .label-red }
[to be deleted]

{: .attention}
> Once you are familiar with the available UI components of this template, exclude this page by changing `nav_order: 99` to `nav_exclude: true` on top of this page (line 3). Its *front matter* will then look like this:
> ```
> ---
> title: UI Components
> nav_exclude: true
> ---
> ```

# UI-Komponenten

Diese Seite beschreibt die wichtigsten Benutzeroberflächenelemente des EasyBuis Task Managers und zeigt, wie sie in der Anwendung dargestellt und verwendet werden.

**Startseite**

Die Startseite des Task Managers bietet einen klar strukturierten Einstiegspunkt für neue und wiederkehrende Benutzer.

![Startseite](images\Startseite.png)

*Elemente:*

Begrüßungstext mit einer kurzen Einführung

Roter Hinweis zur Anmeldung für nicht eingeloggte Benutzer

Zwei Schaltflächen für Anmeldung und Registrierung

Navigationslinks für „Über Uns“, „Kontakt“ und „Impressum“

# Anmeldung und Registrierung

Diese Komponenten ermöglichen es neuen Benutzern, ein Konto zu erstellen, und bestehenden Benutzern, sich anzumelden.

**Anmeldung**

![Log-In](images\Log-In.png)

*Elemente:*

Eingabefelder für E-Mail und Passwort

Schaltflächen für „Anmelden“ und „Zurück zur Startseite“

Link zur Registrierung

**Registrierung**

![Registrierung](images\Registrierung.png)

*Elemente:*

Eingabefelder für E-Mail und Passwort

Checkbox für Nutzungsbedingungen

Schaltflächen für „Registrieren“ und „Zurück zur Startseite“

Link zur Anmeldung

## Kanban-Board

Das Kanban-Board visualisiert den Aufgabenstatus und ermöglicht Drag & Drop zur Statusänderung.

![Kanban-view](images\Kanban-view.png)

*Elemente:*

Spalten für verschiedene Status (To Do, In Progress, In QA, Done)

Schaltflächen für Abmeldung, Admin-Dashboard und Task Manager

Aufgaben als Karten mit Drag & Drop-Funktion

## Aufgabenverwaltung

Die Aufgabenverwaltung ermöglicht das Erstellen, Bearbeiten und Löschen von Aufgaben.

![Task-Manager](images\Task-Manager-Screen.png)

*Elemente:*

Eingabefelder für Titel und Beschreibung einer Aufgabe

Schaltfläche „+ Add Task“

Aufgabenliste mit Schaltflächen für „Edit“ und „Delete“

## Bearbeiten einer Aufgabe

Das Admin-Dashboard ermöglicht es Administratoren, Benutzer zu verwalten und Rollen zu ändern.

![Edit-Task](images\Edit-Task.png)

*Elemente:*

Eingabefelder für Titel und Beschreibung

Statusanzeige der Aufgabe

Checklisten-Elemente mit Option zur Bearbeitung

Schaltflächen für „Speichern“, „Zurück“ und „Neuer Punkt“


## Mermaid-Diagramm

```mermaid
graph TD;
   graph TD;
    A[Startseite] -->|Anmelden| B[Login-Seite]
    A -->|Registrieren| C[Registrierung]
    B -->|Nach Anmeldung| D[Kanban-Board]
    C -->|Nach Registrierung| D
    D -->|Aufgabe erstellen| E[Task Manager]
    E -->|Bearbeiten| F[Aufgabe bearbeiten]
    D -->|Admin-Zugang| G[Admin Dashboard]
    G -->|Benutzerverwaltung| H[Benutzerrollen]
```