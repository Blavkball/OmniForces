# ============================================
# OmniForces
# Housekeeper Test
# ============================================

from memory import MemoryManager, Housekeeper


memory = MemoryManager()

memory.session.set_project(
    "OmniForces"
)

memory.session.set_milestone(
    "Milestone 3"
)

memory.session.add_todo(
    "Test housekeeping"
)


housekeeper = Housekeeper(memory)

housekeeper.run()


print("Housekeeper connected")
print(memory.session.to_dict())

print("Housekeeper test complete")