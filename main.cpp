#include <cassert>
#include <iostream>
#include <vector>

template <typename T>
class Matrix {
private:
    std::vector<std::vector<T>> data;
    size_t n{0}, m{0};

public:
    Matrix() {}

    Matrix(const std::vector<std::vector<T>>& input_data) {
        n = input_data.size(), m = input_data[0].size();
        data.resize(n);
        for (size_t i = 0; i < n; ++i) {
            for (size_t j = 0; j < m; ++j) {
                data[i].push_back(input_data[i][j]);
            }
        }
    }

    T find(size_t i, size_t j) const {
        return data[i][j];
    }

    std::pair<size_t, size_t> size() const {
        return std::pair<size_t, size_t> (n, m);
    }

    Matrix operator+(const Matrix& other) const {
        std::vector<std::vector<T>> summa(n, std::vector<T> (m));
        for (size_t i = 0; i < n; ++i) {
            for (size_t j = 0; j < m; ++j) {
                summa[i][j] = find(i, j) + other.find(i, j);
            }
        }
        return Matrix(summa);
    }

    Matrix& operator+=(const Matrix& other) {
        *this = *this + other;
        return *this;
    }

    template <typename M>
    Matrix operator*(const M& scalar) const {
        std::vector<std::vector<T>> multiplication(n, std::vector<T> (m));
        for (size_t i = 0; i < n; ++i) {
            for (size_t j = 0; j < m; ++j) {
                multiplication[i][j] = find(i, j) * scalar;
            }
        }
        return Matrix(multiplication);
    }

    template <typename M>
    Matrix& operator*=(const M& scalar) {
        *this = *this * scalar;
        return *this;
    }

    Matrix& transpose() {
        std::vector<std::vector<T>> tmp(m, std::vector<T> (n));
        for (size_t i = 0; i < n; ++i) {
            for (size_t j = 0; j < m; ++j) {
                tmp[j][i] = find(i, j);
            }
        }
        *this = Matrix(tmp);
        return *this;
    }

    Matrix transposed() const {
        Matrix tmp = *this;
        tmp.transpose();
        return tmp;
    }

    Matrix operator*(const Matrix& other) const {
        assert(m == other.size().first);
        size_t p = other.size().second;
        std::vector<std::vector<T>> multiplication(n, std::vector<T> (p));
        for (size_t i = 0; i < n; ++i) {
            for (size_t j = 0; j < p; ++j) {
                for (size_t k = 0; k < m; ++k) {
                    multiplication[i][j] += find(i,  k) * other.find(k, j);
                }
            }
        }
        return Matrix(multiplication);
    }

    Matrix& operator*=(const Matrix& other) {
        *this = *this * other;
        return *this;
    }
};

template <typename T>
std::ostream& operator<<(std::ostream& out, const Matrix<T>& m) {
    size_t rows = 0, columns = 0;
    rows = m.size().first, columns = m.size().second;

    if (rows == 0 || columns == 0) {
        return out;
    }

    for (size_t i = 0; i < rows; ++i) {
        if (i > 0) {
            out << '\n';
        }
        out << m.find(i, 0);
        for (size_t j = 1; j < columns; ++j) {
            out << '\t';
            out << m.find(i, j);
        }
    }

    return out;
}