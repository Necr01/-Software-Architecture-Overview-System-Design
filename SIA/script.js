document.addEventListener("DOMContentLoaded", fetchBooks);

function fetchBooks() {
    fetch("/books")
    .then(response => response.json())
    .then(books => {
        const bookList = document.getElementById("bookList");
        bookList.innerHTML = ""; // Clear existing list

        books.forEach(book => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${book.author}</td>
                <td>${book.title}</td>
                <td>${book.category}</td>
                <td>${book.status}</td>
                <td>
                    ${book.status === "Available" 
                        ? `<button class="borrow" onclick="borrowBook(${book.id})">Borrow</button>`
                        : `<button class="return" onclick="returnBook(${book.id})">Return</button>`
                    }
                </td>
            `;
            bookList.appendChild(row);
        });
    });
}


function borrowBook(id) {
    fetch("/borrow", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    }).then(() => fetchBooks());
}

function returnBook(id) {
    fetch("/return", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    }).then(() => fetchBooks());
}

function searchBooks() {
    const query = document.getElementById("search").value.toLowerCase();
    document.querySelectorAll("#bookList tr").forEach(row => {
        row.style.display = row.innerText.toLowerCase().includes(query) ? "" : "none";
    });
}