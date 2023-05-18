#include <cassert>
#include <cstddef>
#include <cstdio>

void enkoder() {
	int last = '\n';
	int ch;
	std::size_t count = 0;

	while ((ch = std::getchar()) != '\n') {
		if (ch != last) {
			if (last != '\n') {
				std::putchar(last);
				std::printf("%zu;", count);
			}

			count = 0;
		}

		++count;
		last = ch;
	}

	if (last != '\n') {
		std::putchar(last);
		std::printf("%zu;", count);
	}

	std::putchar('\n');
}

void dekoder() {
	int ch;

	while ((ch = std::getchar()) != '\n') {
		std::size_t count;
		assert(std::scanf("%zu;", &count) == 1);
		while (count--) std::putchar(ch);
	}

	std::putchar('\n');
}

// rlelib.cpp
//
#include <cassert>
#include <cstdio>

extern void dekoder();
extern void enkoder();

int main() {
	int ch = std::getchar();

	assert(ch == 'D' || ch == 'E');
	assert(std::getchar() == '\n');

	(ch == 'D' ? dekoder : enkoder)();
}
