# from https://www.geeksforgeeks.org/r-program-to-print-the-fibonacci-sequence/

# Function to print the Fibonacci sequence using a loop
print_fibonacci <- function(n) {
    a <- 0
    b <- 1

    cat("Fibonacci Sequence:")
    for (i in 1:n) {
        cat(a, "")
        next_num <- a + b
        a <- b
        b <- next_num
    }
}

number_of_terms <- 10
print_fibonacci(number_of_terms)