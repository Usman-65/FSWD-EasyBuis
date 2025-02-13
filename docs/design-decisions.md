---
title: Design Decisions
nav_order: 3
---

{: .label }
[Jane Dane]

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## 01: [Wahl der Architektur – Flask mit Blueprints]

### Meta

Status: Entschieden
Aktualisiert: 12-Feb-2025

### Problemstellung

Zu Beginn der Entwicklung des EasyBuis Task Managers war unklar, wie die Anwendung modular aufgebaut werden sollte. Die Wahl bestand zwischen einer monolithischen Flask-Anwendung und einer modularen Architektur mit Blueprints.

Ein modulares Design wäre insbesondere hilfreich, um verschiedene Module wie das Kanban-Board, das Benutzerverwaltungssystem und die Aufgabenverwaltung getrennt zu halten und eine bessere Wartbarkeit zu gewährleisten.

### Entscheidung

Wir haben uns für die Nutzung von Flask-Blueprints entschieden.

Begründung:

Eine monolithische Architektur wäre zu unflexibel, insbesondere bei zukünftigen Erweiterungen.

Blueprints ermöglichen eine klare Trennung der Module (z. B. kanban_board.py, task_manager.py, auth_utils.py).

Der Code wird besser strukturiert und wartbarer.

Skalierbarkeit wird erleichtert, da einzelne Komponenten unabhängig optimiert werden können.

Diese Entscheidung wurde nach Abwägung der Alternativen und ersten Implementierungsversuchen getroffen. Zu Beginn wurde versucht, die gesamte Applikation innerhalb einer einzigen app.py Datei zu halten, jedoch führte dies zu wachsender Unübersichtlichkeit.

### Betrachtete Optionen

|| Kriterium        | Monolithische Architektur | Flask mit Blueprints |
|-----------------|--------------------------|----------------------|
| **Wartbarkeit** | ❌ Schwer skalierbar     | ✔️ Klare Trennung der Module |
| **Flexibilität** | ❌ Änderungen sind umständlich | ✔️ Einfache Erweiterung |
| **Skalierbarkeit** | ❌ Begrenzte Skalierbarkeit | ✔️ Einfacher modular erweiterbar |

---

## 02: [Datenbankzugriff – SQL oder SQLAlchemy]

### Meta

Status: Entschieden
Aktualisiert: 10-Jan-2025

**Problemstellung**

Eine zentrale Entscheidung war, ob für die Datenbankabfragen reines SQL oder SQLAlchemy als ORM verwendet werden sollte. Während SQLAlchemy viele Vorteile hinsichtlich Abstraktion und Kompatibilität mit anderen Datenbanksystemen bietet, wäre die direkte Nutzung von SQL einfacher umzusetzen.

**Entscheidung**

Wir haben uns entschieden, reines SQL zu verwenden.

Begründung:

SQL ist bereits bekannt und erfordert keine zusätzliche Einarbeitung.

Die Anwendung nutzt SQLite, sodass ORM-Funktionen derzeit nicht notwendig sind.

Eine spätere Umstellung auf ein ORM ist möglich, falls ein Wechsel zu PostgreSQL oder MySQL erfolgt.

## Betrachtete Optionen
| Kriterium                  | Plain SQL                | SQLAlchemy               |
|----------------------------|--------------------------|--------------------------|
| **Einfachheit**            | ✔️ Direkt verständlich  | ❌ Lernaufwand nötig    |
| **Erfahrungen**   | ✔️ schon gesammelt  | ❌ wenig Erfahrung |
| **Flexibilität für zukünftige DBs** | ❌ Muss umgeschrieben werden | ✔️ Einfacher Wechsel |

---

## 03: [Datenbankzugriff – Benutzerrollen und Berechtigungen]

## Meta

Status: Entschieden
Aktualisiert: 02-Feb-2025

**Problemstellung**

Wie sollte die Zugriffskontrolle für verschiedene Benutzerrollen umgesetzt werden? Die Herausforderung bestand darin, eine sichere, aber auch flexible Lösung zu finden.

Anfangs wurde eine einfache Benutzerverwaltung ohne Rollenmodell benutzt, jedoch wurde schnell klar, dass verschiedene Berechtigungen für Administratoren, Manager und Benutzer notwendig sind.

**Entscheidung**

Wir haben uns für ein rollenbasiertes Berechtigungssystem entschieden, implementiert durch eine separate auth_utils.py Datei mit einem requires_permission Decorator.

Begründung:

Die Zugriffskontrolle kann zentral gesteuert und leicht erweitert werden.

Administratoren können Benutzer verwalten, während normale Benutzer nur ihre eigenen Aufgaben sehen/bearbeiten können.

Rollen wie „Leser“ ermöglichen es, dass gewisse Benutzer nur Ansichtsrechte haben.

## Betrachtete Optionen

## Betrachtete Optionen

<table>
  <tr>
    <th>Kriterium</th>
    <th>Keine Rollen</th>
    <th>Rollenbasiertes System</th>
  </tr>
  <tr>
    <td><b>Sicherheit</b></td>
    <td>❌ Jeder hat die gleichen Rechte</td>
    <td>✅ Zugriffsbeschränkungen</td>
  </tr>
  <tr>
    <td><b>Erweiterbarkeit</b></td>
    <td>❌ Schwer skalierbar</td>
    <td>✅ Neue Rollen können leicht hinzugefügt werden</td>
  </tr>
  <tr>
    <td><b>Code-Wartbarkeit</b></td>
    <td>✅ Einfacher Code</td>
    <td>❌ Etwas mehr Implementierungsaufwand</td>
  </tr>
</table>
