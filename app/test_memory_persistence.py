# ============================================
# OmniForces
# Memory Persistence Test
# ============================================

from memory import MemoryManager


memory = MemoryManager()

# Add information
memory.session.set_project("OmniForces")
memory.session.set_milestone("Milestone 3 Persistence Test")

memory.long_term.add_knowledge(
    "test",
    "Memory survived save and reload"
)

# Save
memory.save()

print("Memory saved")

# Create a new memory manager
new_memory = MemoryManager()

# Load saved data
new_memory.load()

print(new_memory.session.to_dict())
print(new_memory.long_term.to_dict())

print("Persistence test complete")