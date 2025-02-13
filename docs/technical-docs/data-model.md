---
title: Data Model
parent: Technical Docs
nav_order: 2
---


{: .no_toc }
# Data model

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Überblick

Das Datenmodell des EasyBuis Task Managers bildet die Struktur der gespeicherten Daten ab und stellt sicher, dass alle relevanten Informationen effizient und konsistent verwaltet werden. Die Anwendung nutzt SQLite als Datenbank zur Speicherung von Benutzern, Aufgaben und zugehörigen Checklisten.

## Entitäten und Beziehungen

Die folgende Darstellung zeigt das Entity-Relationship-Diagramm (ERD) der wichtigsten Tabellen und deren Beziehungen:

![ERD](../images\ERD.png)


## Datenintegrität und Einschränkungen

**Eindeutigkeit**: Die E-Mail-Adresse eines Benutzers ist einzigartig.

**Referentielle Integrität**: Die task_id in der checklist-Tabelle ist ein Fremdschlüssel, der sicherstellt, dass jedes Element einer bestehenden Aufgabe zugeordnet ist.

**Datenvalidierung**: Die status-Felder der Tabellen tasks und checklist sind eingeschränkt auf vordefinierte Werte zur Vermeidung von Inkonsistenzen.

