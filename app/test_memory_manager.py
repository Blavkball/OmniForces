# ============================================
# OmniForces
# Memory Manager Integration Test
# ============================================

from memory import MemoryManager


memory = MemoryManager()

# Working memory
memory.working.set_task(
    "Testing MemoryManager integration"
)

memory.working.add_note(
    "All memory systems should connect through MemoryManager"
)


# Session memory
memory.session.set_project(
    "OmniForces"
)

memory.session.set_milestone(
    "Milestone 3"
)

memory.session.add_todo(
    "Complete memory subsystem"
)


# Long term memory
memory.long_term.add_knowledge(
    "architecture",
    "Agents communicate through MemoryManager"
)


# Save everything
memory.save()


# Display results
print("WORKING MEMORY")
print(memory.working.to_dict())

print("\nSESSION MEMORY")
print(memory.session.to_dict())

print("\nLONG TERM MEMORY")
print(memory.long_term.to_dict())

print("\nMemoryManager integration test complete")