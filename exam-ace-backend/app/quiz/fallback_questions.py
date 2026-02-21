"""
Fallback question bank — curated questions used when the local LLM is unreachable.
Organized by subject × difficulty. Randomly samples `count` questions.
"""
from __future__ import annotations

import random
import logging
from app.quiz.models import Difficulty, QuizQuestion

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Question Bank — keyed by (subject_lowercase, difficulty)
# ---------------------------------------------------------------------------

_BANK: dict[tuple[str, Difficulty], list[QuizQuestion]] = {}


def _add(subject: str, difficulty: Difficulty, questions: list[dict]) -> None:
    key = (subject.lower(), difficulty)
    _BANK[key] = [QuizQuestion(**q) for q in questions]


# ===== COMPUTER SCIENCE =====

_add("computer science", Difficulty.beginner, [
    {"question": "What does CPU stand for?", "options": ["Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Computer Processing Utility"], "correct_index": 0, "explanation": "CPU stands for Central Processing Unit, the primary component that executes instructions."},
    {"question": "Which data structure uses FIFO (First In, First Out)?", "options": ["Stack", "Queue", "Tree", "Graph"], "correct_index": 1, "explanation": "A Queue follows FIFO ordering — the first element added is the first removed."},
    {"question": "What is the binary representation of the decimal number 10?", "options": ["1010", "1100", "1001", "1110"], "correct_index": 0, "explanation": "10 in binary is 1010 (8+2)."},
    {"question": "Which language is primarily used for web page styling?", "options": ["HTML", "JavaScript", "CSS", "Python"], "correct_index": 2, "explanation": "CSS (Cascading Style Sheets) is the standard language for styling web pages."},
    {"question": "What does RAM stand for?", "options": ["Read Access Memory", "Random Access Memory", "Run Application Memory", "Rapid Access Module"], "correct_index": 1, "explanation": "RAM stands for Random Access Memory, a type of volatile storage."},
    {"question": "Which of the following is an operating system?", "options": ["Python", "Linux", "HTML", "MySQL"], "correct_index": 1, "explanation": "Linux is an open-source operating system kernel used in many distributions."},
    {"question": "What is the smallest unit of data in a computer?", "options": ["Byte", "Bit", "Kilobyte", "Nibble"], "correct_index": 1, "explanation": "A bit (binary digit) is the smallest unit, representing a 0 or 1."},
    {"question": "Which symbol is used for single-line comments in Python?", "options": ["//", "#", "--", "/*"], "correct_index": 1, "explanation": "Python uses the # symbol for single-line comments."},
])

_add("computer science", Difficulty.intermediate, [
    {"question": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"], "correct_index": 1, "explanation": "Binary search halves the search space each step, giving O(log n) complexity."},
    {"question": "Which protocol is used for secure web communication?", "options": ["HTTP", "FTP", "HTTPS", "SMTP"], "correct_index": 2, "explanation": "HTTPS uses TLS/SSL encryption on top of HTTP for secure communication."},
    {"question": "In OOP, what does encapsulation mean?", "options": ["Inheriting from a parent class", "Bundling data and methods that operate on that data", "Creating multiple instances", "Overriding parent methods"], "correct_index": 1, "explanation": "Encapsulation is the bundling of data with the methods that act on it, restricting direct access."},
    {"question": "What is a foreign key in a relational database?", "options": ["A unique identifier for a row", "A key that references the primary key of another table", "An encrypted column", "The first column in a table"], "correct_index": 1, "explanation": "A foreign key creates a link between two tables by referencing the primary key of another table."},
    {"question": "What does DNS stand for?", "options": ["Data Network System", "Domain Name System", "Digital Naming Service", "Distributed Node Structure"], "correct_index": 1, "explanation": "DNS translates domain names (like google.com) into IP addresses."},
    {"question": "Which sorting algorithm has the best average-case time complexity?", "options": ["Bubble Sort", "Selection Sort", "Merge Sort", "Insertion Sort"], "correct_index": 2, "explanation": "Merge Sort has O(n log n) average-case complexity, better than the O(n²) of bubble/selection/insertion sort."},
    {"question": "What is a deadlock in operating systems?", "options": ["A fast execution state", "When two or more processes are waiting indefinitely for each other", "A type of memory allocation", "A CPU scheduling algorithm"], "correct_index": 1, "explanation": "Deadlock occurs when processes hold resources while waiting for others, creating a circular dependency."},
    {"question": "Which of these is a NoSQL database?", "options": ["PostgreSQL", "MySQL", "MongoDB", "SQLite"], "correct_index": 2, "explanation": "MongoDB is a document-based NoSQL database that stores data in flexible JSON-like documents."},
])

_add("computer science", Difficulty.advanced, [
    {"question": "What is the CAP theorem about?", "options": ["CPU, ALU, and Pipeline design", "Consistency, Availability, and Partition tolerance trade-offs", "Cache, Address, and Protocol optimization", "Computation, Algorithm, and Performance analysis"], "correct_index": 1, "explanation": "CAP theorem states a distributed system can only guarantee two of: Consistency, Availability, Partition tolerance."},
    {"question": "Which consensus algorithm does Raft implement?", "options": ["Byzantine fault tolerance", "Leader-based log replication", "Proof of work", "Two-phase commit"], "correct_index": 1, "explanation": "Raft is a leader-based consensus algorithm that replicates a log across a cluster of servers."},
    {"question": "What is the purpose of a Bloom filter?", "options": ["Sorting data efficiently", "Probabilistic set membership testing", "Compressing files", "Encrypting data"], "correct_index": 1, "explanation": "A Bloom filter is a space-efficient probabilistic data structure that tests whether an element is a member of a set, with possible false positives but no false negatives."},
    {"question": "In lambda calculus, what is a beta reduction?", "options": ["Removing unused variables", "Applying a function to its argument", "Renaming bound variables", "Converting to normal form"], "correct_index": 1, "explanation": "Beta reduction is the process of applying a lambda abstraction to an argument by substituting the bound variable."},
    {"question": "What does the ACID property 'Isolation' guarantee?", "options": ["Transactions are stored permanently", "Concurrent transactions don't interfere with each other", "All operations in a transaction succeed or none do", "Data remains valid after a transaction"], "correct_index": 1, "explanation": "Isolation ensures concurrent transactions execute as if they were serial, preventing dirty reads and other anomalies."},
    {"question": "Which problem is NP-complete?", "options": ["Binary search", "Sorting an array", "Travelling Salesman Problem (decision version)", "Finding the maximum in a list"], "correct_index": 2, "explanation": "The decision version of TSP ('Is there a tour shorter than k?') is NP-complete."},
    {"question": "What is the difference between a mutex and a semaphore?", "options": ["They are identical", "A mutex is binary; a semaphore can have a count > 1", "A semaphore is faster", "A mutex allows multiple threads"], "correct_index": 1, "explanation": "A mutex is a binary lock (0 or 1), while a counting semaphore allows a specified number of concurrent accesses."},
    {"question": "What is tail call optimization?", "options": ["Caching function results", "Reusing the current stack frame for recursive calls in tail position", "Parallelizing function calls", "Inlining small functions"], "correct_index": 1, "explanation": "TCO reuses the current stack frame when a function's last action is a recursive call, preventing stack overflow."},
])

# ===== MATHEMATICS =====

_add("mathematics", Difficulty.beginner, [
    {"question": "What is the value of π (pi) rounded to two decimal places?", "options": ["3.14", "3.41", "2.71", "3.17"], "correct_index": 0, "explanation": "Pi is approximately 3.14159..., which rounds to 3.14."},
    {"question": "What is 15% of 200?", "options": ["15", "25", "30", "35"], "correct_index": 2, "explanation": "15% of 200 = 0.15 × 200 = 30."},
    {"question": "What is the square root of 144?", "options": ["14", "12", "11", "13"], "correct_index": 1, "explanation": "12 × 12 = 144, so √144 = 12."},
    {"question": "In a right triangle, what is the longest side called?", "options": ["Adjacent", "Opposite", "Hypotenuse", "Base"], "correct_index": 2, "explanation": "The hypotenuse is the side opposite the right angle and the longest side of a right triangle."},
    {"question": "What is the sum of angles in a triangle?", "options": ["90°", "180°", "270°", "360°"], "correct_index": 1, "explanation": "The sum of interior angles of any triangle is always 180 degrees."},
    {"question": "What is 7 factorial (7!)?", "options": ["720", "5040", "40320", "3628800"], "correct_index": 1, "explanation": "7! = 7×6×5×4×3×2×1 = 5040."},
    {"question": "What is the next prime number after 7?", "options": ["8", "9", "10", "11"], "correct_index": 3, "explanation": "11 is the next prime after 7 (8, 9, and 10 are all composite)."},
])

_add("mathematics", Difficulty.intermediate, [
    {"question": "What is the derivative of x³?", "options": ["x²", "3x²", "3x", "x³/3"], "correct_index": 1, "explanation": "Using the power rule, d/dx(x³) = 3x²."},
    {"question": "What is the integral of 2x dx?", "options": ["x² + C", "2x² + C", "x + C", "2x + C"], "correct_index": 0, "explanation": "∫2x dx = 2·(x²/2) + C = x² + C."},
    {"question": "What is log₂(64)?", "options": ["4", "5", "6", "8"], "correct_index": 2, "explanation": "2⁶ = 64, so log₂(64) = 6."},
    {"question": "What is the determinant of the matrix [[1,2],[3,4]]?", "options": ["-2", "2", "-1", "10"], "correct_index": 0, "explanation": "det = (1×4) - (2×3) = 4 - 6 = -2."},
    {"question": "In how many ways can 5 people be arranged in a line?", "options": ["25", "60", "120", "720"], "correct_index": 2, "explanation": "This is 5P5 = 5! = 120."},
    {"question": "What is the formula for the sum of an arithmetic series?", "options": ["n(n+1)/2", "n/2 × (first + last)", "a × rⁿ", "n² + 1"], "correct_index": 1, "explanation": "Sum = n/2 × (a₁ + aₙ), where n is the number of terms."},
    {"question": "What is the quadratic formula?", "options": ["x = -b/2a", "x = (-b ± √(b²-4ac)) / 2a", "x = -c/b", "x = b² - 4ac"], "correct_index": 1, "explanation": "The quadratic formula solves ax² + bx + c = 0 for x."},
])

_add("mathematics", Difficulty.advanced, [
    {"question": "What is the Euler's identity?", "options": ["e^(iπ) = -1", "e^(iπ) = 1", "e^(iπ) = 0", "e^(iπ) = i"], "correct_index": 0, "explanation": "Euler's identity states e^(iπ) + 1 = 0, or equivalently e^(iπ) = -1."},
    {"question": "What is the rank of a 3×3 identity matrix?", "options": ["1", "2", "3", "0"], "correct_index": 2, "explanation": "The identity matrix has 3 linearly independent rows/columns, so its rank is 3."},
    {"question": "What is the Riemann Hypothesis about?", "options": ["Distribution of prime numbers", "Convergence of infinite series", "Topology of manifolds", "Graph coloring"], "correct_index": 0, "explanation": "The Riemann Hypothesis conjectures that all non-trivial zeros of the zeta function have real part 1/2, relating to prime distribution."},
    {"question": "What is a Hilbert space?", "options": ["A 3D Euclidean space", "A complete inner product space", "A discrete topology", "A finite vector space"], "correct_index": 1, "explanation": "A Hilbert space is a complete (every Cauchy sequence converges) inner product space, generalizing Euclidean space to infinite dimensions."},
    {"question": "What is the Lebesgue integral's advantage over Riemann?", "options": ["Faster computation", "Handles more functions and has better limit theorems", "Only works in 1D", "Requires continuity"], "correct_index": 1, "explanation": "The Lebesgue integral can integrate a wider class of functions and supports powerful convergence theorems (DCT, MCT)."},
    {"question": "What is the order of the symmetric group S₅?", "options": ["25", "60", "120", "720"], "correct_index": 2, "explanation": "|S₅| = 5! = 120."},
    {"question": "What does Gödel's incompleteness theorem state?", "options": ["All true statements are provable", "Any consistent system powerful enough to express arithmetic contains unprovable truths", "Mathematics is inconsistent", "Every equation has a solution"], "correct_index": 1, "explanation": "Gödel showed that in any consistent formal system capable of expressing basic arithmetic, there exist true statements that cannot be proved within the system."},
])

# ===== PHYSICS =====

_add("physics", Difficulty.beginner, [
    {"question": "What is the SI unit of force?", "options": ["Joule", "Watt", "Newton", "Pascal"], "correct_index": 2, "explanation": "The Newton (N) is the SI unit of force: 1 N = 1 kg·m/s²."},
    {"question": "What is the speed of light in vacuum (approximately)?", "options": ["3 × 10⁶ m/s", "3 × 10⁸ m/s", "3 × 10¹⁰ m/s", "3 × 10⁴ m/s"], "correct_index": 1, "explanation": "The speed of light in vacuum is approximately 3 × 10⁸ m/s (299,792,458 m/s)."},
    {"question": "Which law states 'Every action has an equal and opposite reaction'?", "options": ["Newton's First Law", "Newton's Second Law", "Newton's Third Law", "Law of Gravitation"], "correct_index": 2, "explanation": "Newton's Third Law of Motion describes action-reaction force pairs."},
    {"question": "What is the unit of electrical resistance?", "options": ["Volt", "Ampere", "Ohm", "Watt"], "correct_index": 2, "explanation": "The Ohm (Ω) is the SI unit of electrical resistance."},
    {"question": "What type of energy does a moving car have?", "options": ["Potential energy", "Kinetic energy", "Thermal energy", "Nuclear energy"], "correct_index": 1, "explanation": "A moving object possesses kinetic energy, KE = ½mv²."},
    {"question": "What is the boiling point of water at standard pressure?", "options": ["90°C", "100°C", "110°C", "120°C"], "correct_index": 1, "explanation": "Water boils at 100°C (212°F) at standard atmospheric pressure."},
    {"question": "What does DC stand for in electricity?", "options": ["Double Current", "Direct Current", "Dense Charge", "Dynamic Circuit"], "correct_index": 1, "explanation": "DC stands for Direct Current, where the electric charge flows in one direction."},
])

_add("physics", Difficulty.intermediate, [
    {"question": "What is the formula for gravitational potential energy?", "options": ["E = mc²", "PE = mgh", "KE = ½mv²", "F = ma"], "correct_index": 1, "explanation": "Gravitational potential energy near Earth's surface is PE = mgh (mass × gravity × height)."},
    {"question": "What is Ohm's Law?", "options": ["V = IR", "P = IV", "F = qE", "E = hf"], "correct_index": 0, "explanation": "Ohm's Law states voltage = current × resistance (V = IR)."},
    {"question": "Which particle has no electric charge?", "options": ["Proton", "Electron", "Neutron", "Positron"], "correct_index": 2, "explanation": "The neutron is electrically neutral (no charge), found in the atomic nucleus."},
    {"question": "What is the principle behind a hydraulic press?", "options": ["Archimedes' principle", "Pascal's law", "Bernoulli's principle", "Boyle's law"], "correct_index": 1, "explanation": "Pascal's law states that pressure applied to a confined fluid is transmitted equally in all directions."},
    {"question": "What is the frequency of a wave with wavelength 2m and speed 340 m/s?", "options": ["170 Hz", "680 Hz", "85 Hz", "340 Hz"], "correct_index": 0, "explanation": "f = v/λ = 340/2 = 170 Hz."},
    {"question": "What phenomenon explains why the sky is blue?", "options": ["Reflection", "Refraction", "Rayleigh scattering", "Diffraction"], "correct_index": 2, "explanation": "Rayleigh scattering causes shorter blue wavelengths to scatter more than longer red wavelengths."},
    {"question": "What is the first law of thermodynamics?", "options": ["Entropy always increases", "Energy cannot be created or destroyed", "Absolute zero is unattainable", "Heat flows from hot to cold"], "correct_index": 1, "explanation": "The first law states that energy is conserved: ΔU = Q - W."},
])

_add("physics", Difficulty.advanced, [
    {"question": "What is the Heisenberg Uncertainty Principle?", "options": ["Energy is always conserved", "You cannot simultaneously know exact position and momentum of a particle", "Light is both a wave and particle", "Entropy always increases"], "correct_index": 1, "explanation": "The uncertainty principle states Δx·Δp ≥ ℏ/2, limiting simultaneous precision of position and momentum."},
    {"question": "What is the Schwarzschild radius?", "options": ["The radius of a neutron star", "The event horizon radius of a non-rotating black hole", "The radius of the observable universe", "The Bohr radius of hydrogen"], "correct_index": 1, "explanation": "The Schwarzschild radius (r_s = 2GM/c²) defines the event horizon of a non-rotating black hole."},
    {"question": "In special relativity, what happens to mass as an object approaches the speed of light?", "options": ["It decreases", "It stays the same", "Its relativistic mass increases without bound", "It becomes negative"], "correct_index": 2, "explanation": "As v → c, the Lorentz factor γ → ∞, and the relativistic momentum (and effective inertia) increases without bound."},
    {"question": "What is the significance of the fine-structure constant α ≈ 1/137?", "options": ["It defines the speed of light", "It characterizes the strength of electromagnetic interaction", "It determines nuclear stability", "It sets the Planck scale"], "correct_index": 1, "explanation": "The fine-structure constant α ≈ 1/137 is a dimensionless constant characterizing the strength of the electromagnetic force."},
    {"question": "What is quantum entanglement?", "options": ["Particles orbiting each other", "Correlated quantum states where measuring one instantly affects the other", "Particles merging together", "A type of nuclear reaction"], "correct_index": 1, "explanation": "Entangled particles have correlated quantum states: measuring one determines the state of the other, regardless of distance."},
    {"question": "What does the Dirac equation describe?", "options": ["Classical fluid dynamics", "Relativistic quantum mechanics of spin-½ particles", "Gravitational waves", "Thermodynamic equilibrium"], "correct_index": 1, "explanation": "The Dirac equation is a relativistic wave equation describing fermions (spin-½ particles) like electrons, predicting antimatter."},
    {"question": "What is the cosmological constant problem?", "options": ["Dark matter hasn't been found", "The observed vacuum energy is ~120 orders of magnitude smaller than predicted", "The universe's age is unknown", "Gravity hasn't been quantized"], "correct_index": 1, "explanation": "Quantum field theory predicts a vacuum energy density vastly larger than observed, one of the biggest unsolved problems."},
])

# ===== GENERAL KNOWLEDGE =====

_add("general knowledge", Difficulty.beginner, [
    {"question": "Which planet is known as the Red Planet?", "options": ["Venus", "Mars", "Jupiter", "Saturn"], "correct_index": 1, "explanation": "Mars appears red due to iron oxide (rust) on its surface."},
    {"question": "What is the largest ocean on Earth?", "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"], "correct_index": 3, "explanation": "The Pacific Ocean is the largest, covering about 63 million square miles."},
    {"question": "Who wrote 'Romeo and Juliet'?", "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"], "correct_index": 1, "explanation": "William Shakespeare wrote Romeo and Juliet, believed to be written between 1591 and 1596."},
    {"question": "What is the chemical symbol for gold?", "options": ["Go", "Gd", "Au", "Ag"], "correct_index": 2, "explanation": "Au comes from the Latin word 'aurum' meaning gold."},
    {"question": "Which gas do plants absorb from the atmosphere?", "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], "correct_index": 2, "explanation": "Plants absorb CO₂ during photosynthesis and release oxygen."},
    {"question": "How many continents are there on Earth?", "options": ["5", "6", "7", "8"], "correct_index": 2, "explanation": "There are 7 continents: Africa, Antarctica, Asia, Australia, Europe, North America, South America."},
    {"question": "What is the tallest mountain in the world?", "options": ["K2", "Kangchenjunga", "Mount Everest", "Lhotse"], "correct_index": 2, "explanation": "Mount Everest stands at 8,849 meters (29,032 feet) above sea level."},
])

_add("general knowledge", Difficulty.intermediate, [
    {"question": "What is the Fibonacci sequence's next number after 1, 1, 2, 3, 5, 8?", "options": ["11", "12", "13", "15"], "correct_index": 2, "explanation": "Each number is the sum of the two preceding ones: 5 + 8 = 13."},
    {"question": "Which element has the atomic number 79?", "options": ["Silver", "Gold", "Platinum", "Copper"], "correct_index": 1, "explanation": "Gold (Au) has atomic number 79."},
    {"question": "What is the longest river in the world?", "options": ["Amazon", "Nile", "Yangtze", "Mississippi"], "correct_index": 1, "explanation": "The Nile River is approximately 6,650 km (4,130 mi) long, the longest in the world."},
    {"question": "Who developed the theory of general relativity?", "options": ["Isaac Newton", "Niels Bohr", "Albert Einstein", "Max Planck"], "correct_index": 2, "explanation": "Albert Einstein published the theory of general relativity in 1915."},
    {"question": "What is the smallest country in the world by area?", "options": ["Monaco", "Vatican City", "San Marino", "Liechtenstein"], "correct_index": 1, "explanation": "Vatican City is the smallest country, at about 44 hectares (110 acres)."},
    {"question": "What is the main component of the Sun?", "options": ["Helium", "Hydrogen", "Oxygen", "Carbon"], "correct_index": 1, "explanation": "The Sun is about 73% hydrogen and 25% helium by mass."},
    {"question": "In what year did World War II end?", "options": ["1943", "1944", "1945", "1946"], "correct_index": 2, "explanation": "World War II ended in 1945 with the surrender of Germany in May and Japan in September."},
])

_add("general knowledge", Difficulty.advanced, [
    {"question": "What is the Chandrasekhar limit?", "options": ["Maximum mass of a white dwarf (~1.4 solar masses)", "Maximum speed in the universe", "Age of the universe", "Size of the observable universe"], "correct_index": 0, "explanation": "The Chandrasekhar limit (~1.4 M☉) is the maximum mass of a stable white dwarf star."},
    {"question": "Which treaty established the European Economic Community?", "options": ["Treaty of Versailles", "Treaty of Rome", "Maastricht Treaty", "Treaty of Lisbon"], "correct_index": 1, "explanation": "The Treaty of Rome (1957) established the EEC, a precursor to the EU."},
    {"question": "What is CRISPR-Cas9 used for?", "options": ["Quantum computing", "Gene editing", "Nuclear fusion", "Cryptocurrency mining"], "correct_index": 1, "explanation": "CRISPR-Cas9 is a revolutionary gene-editing technology that can precisely modify DNA sequences."},
    {"question": "Who is considered the father of modern economics?", "options": ["Karl Marx", "Adam Smith", "John Maynard Keynes", "Milton Friedman"], "correct_index": 1, "explanation": "Adam Smith, author of 'The Wealth of Nations' (1776), is widely considered the father of modern economics."},
    {"question": "What is the Drake Equation used to estimate?", "options": ["Age of the universe", "Number of communicative civilizations in the Milky Way", "Speed of galaxy expansion", "Entropy of the universe"], "correct_index": 1, "explanation": "The Drake Equation estimates the number of active, communicative extraterrestrial civilizations in the Milky Way."},
    {"question": "What is the Sapir-Whorf hypothesis?", "options": ["A theory about evolution", "Language influences thought and perception", "A principle of thermodynamics", "A model of the atom"], "correct_index": 1, "explanation": "The Sapir-Whorf hypothesis proposes that the structure of a language affects its speakers' cognition and worldview."},
    {"question": "What is the significance of the Rosetta Stone?", "options": ["It predicted eclipses", "It enabled decipherment of Egyptian hieroglyphs", "It described ancient Greek democracy", "It mapped trade routes"], "correct_index": 1, "explanation": "The Rosetta Stone (196 BC) had text in three scripts, enabling Jean-François Champollion to decipher hieroglyphs in 1822."},
])


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_fallback_questions(subject: str, difficulty: Difficulty, count: int) -> list[QuizQuestion]:
    """
    Return `count` randomly sampled questions from the bank.
    Falls back to a broader search if the exact subject isn't found.
    """
    key = (subject.lower(), difficulty)
    pool = _BANK.get(key)

    # If exact subject not found, try a loose match
    if not pool:
        for (s, d), qs in _BANK.items():
            if d == difficulty and subject.lower() in s:
                pool = qs
                break

    # Last resort: use general knowledge for the difficulty
    if not pool:
        pool = _BANK.get(("general knowledge", difficulty), [])

    if not pool:
        # Absolute last resort: grab everything for the difficulty
        pool = []
        for (_, d), qs in _BANK.items():
            if d == difficulty:
                pool.extend(qs)

    if len(pool) < count:
        logger.warning("Only %d fallback questions available for %s/%s, requested %d", len(pool), subject, difficulty.value, count)
        count = min(count, len(pool))

    if count == 0:
        raise RuntimeError(f"No fallback questions available for {subject}/{difficulty.value}")

    return random.sample(pool, count)
