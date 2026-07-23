# Raw Architecture

Version:
1.0

Status:
Architecture Draft

Source of Truth:

AI_Workstation is the master company documentation system.

This document defines the Raw subsystem of the OmniForces Brain.

---

# Purpose

Raw is the permanent evidence repository for OmniForces.

Its responsibility is to preserve every piece of information exactly as it was received.

Raw is not responsible for organisation, classification, summarisation or execution.

Its only responsibility is preservation.

---

# Core Principle

> Raw never changes.

Everything received is stored permanently as the original source of truth.

All intelligence is performed outside of Raw.

---

# Responsibilities

Raw must:

- Store original information.
- Preserve original content.
- Assign unique identifiers.
- Record metadata.
- Maintain an audit history.
- Provide traceable evidence.
- Supply information to the Brain.

Raw does not:

- Organise information.
- Generate summaries.
- Create Wiki pages.
- Execute tasks.
- Make decisions.
- Modify stored content.

---

# Immutable Rule

Once information enters Raw it must never be:

- Edited.
- Renamed.
- Rewritten.
- Reformatted.
- Moved.
- Replaced.
- Deleted without explicit human approval.

Raw is permanent evidence.

---

# Accepted Input

Raw accepts any supported information including:

- Plain text
- Markdown
- Source code
- PDFs
- Word documents
- Images
- Audio
- Video
- URLs
- Emails
- Chat conversations
- Meeting notes
- Project ideas
- Tasks
- Specifications
- Logs
- Configuration files

Future versions may support additional formats.

---

# Raw Record Structure

Every Raw item contains:

```
Raw ID
Title
Original Filename
Original Content
Content Type
Source
Created By
Created Date
Checksum
Tags (System Generated)
Processing Status
Linked Wiki Pages
Audit History
```

---

# Example Record

```json
{
  "raw_id": "RAW-000001",
  "title": "Meeting Notes",
  "original_filename": "meeting.md",
  "content_type": "text/markdown",
  "source": "User Upload",
  "created_by": "Human",
  "created_at": "2026-07-23T14:00:00Z",
  "checksum": "sha256...",
  "processing_status": "Pending",
  "linked_wiki_pages": [],
  "audit_history": []
}
```

---

# Unique Identifier

Every Raw record receives a permanent unique identifier.

Example:

```
RAW-000001
RAW-000002
RAW-000003
```

Identifiers are never reused.

---

# Metadata

Metadata may include:

- Creation date
- Creator
- Import source
- File size
- File type
- Hash
- Processing status
- Related projects
- Related Atomic Tasks

Metadata may be updated.

Original content may not.

---

# Processing Status

Each record has a processing state.

Possible values:

```
Received

Queued

Processing

Processed

Archived

Error
```

Processing status does not change the stored content.

---

# Audit Trail

Every operation performed against a Raw record is logged.

Examples:

- Imported
- Viewed
- Linked
- Indexed
- Referenced
- Approved for deletion

The audit trail must never be removed.

---

# Relationships

Raw records may be linked to:

- Wiki pages
- Atomic Tasks
- Projects
- AI Employees
- Decisions
- Documents

These relationships exist outside the original content.

---

# Security

Every Raw record must have:

- Verified origin
- Unique identifier
- Permission controls
- Audit history

Only authorised systems may read or reference Raw.

---

# Integration

Raw supplies information to:

- Wiki
- Memory System
- Supervisor
- Agent Manager
- Atomic Task Engine
- Resume Engine

Raw never controls those systems.

---

# Recovery

Because Raw preserves original information, the Brain can always rebuild:

- Wiki
- Relationships
- Indexes
- Knowledge Graph
- Search Database

Raw is the permanent recovery source.

---

# Future Expansion

Future versions may include:

- Version verification
- Content fingerprinting
- Duplicate detection
- Automatic import connectors
- OCR processing
- Speech transcription
- Large file streaming
- Distributed storage

These features extend Raw without changing its core responsibility.

---

# Final Principle

> Raw is the permanent evidence layer of OmniForces. Every piece of information is preserved exactly as received, providing an immutable foundation from which all knowledge, relationships and automation are built.