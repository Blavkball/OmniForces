# ============================================
# OmniForces
# Memory System Test
# ============================================

from memory import MemoryManager


memory = MemoryManager()

memory.session.set_project("OmniForces")
memory.session.set_milestone("Milestone 3")

memory.working.set_task("Testing Memory System")

memory.long_term.add_knowledge(
    "architecture",
    "MemoryManager controls all memory access"
)

print(memory.working.to_dict())
print(memory.session.to_dict())
print(memory.long_term.to_dict())

memory.save()

print("Memory test complete")