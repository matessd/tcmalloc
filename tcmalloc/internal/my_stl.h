#ifndef TCMALLOC_INTERNAL_ALGORITHM_H_
#define TCMALLOC_INTERNAL_ALGORITHM_H_

#include <stddef.h>
#include <stdint.h>

#include "absl/base/attributes.h"
#include "absl/base/optimization.h"
#include "tcmalloc/internal/logging.h"
#include <set>
#include <map>

namespace tcmalloc {
// sun:
typedef std::set<uintptr_t> HpSet;
typedef std::map<uintptr_t,size_t> HpMap;

// A well-typed and sorted intrusive doubly linked list.
template <typename T, typename Comp>
class TSortedList {
 private:
  class Iter;

 public:
  // The intrusive element supertype.  Use the CRTP to declare your class:
  // class MyListItems : public TSortedList<MyListItems, Functor>::Elem { ...
  class Elem {
    friend class Iter;
    friend class TSortedList<T, Comp>;
    Elem *next_;
    Elem *prev_;

   protected:
    constexpr Elem() : next_(nullptr), prev_(nullptr) {}

    // Returns true iff the list is empty after removing this
    bool remove() {
      // Copy out next/prev before doing stores, otherwise compiler assumes
      // potential aliasing and does unnecessary reloads after stores.
      Elem *next = next_;
      Elem *prev = prev_;
      ASSERT(prev->next_ == this);
      prev->next_ = next;
      ASSERT(next->prev_ == this);
      next->prev_ = prev;
#ifndef NDEBUG
      prev_ = nullptr;
      next_ = nullptr;
#endif
      return next == prev;
    }

    void prepend(Elem *item) {
      Elem *prev = prev_;
      item->prev_ = prev;
      item->next_ = this;
      prev->next_ = item;
      prev_ = item;
    }

    void append(Elem *item) {
      Elem *next = next_;
      item->next_ = next;
      item->prev_ = this;
      next->prev_ = item;
      next_ = item;
    }
  };

  // Initialize to empty list.
  constexpr TSortedList() { head_.next_ = head_.prev_ = &head_; }

  bool empty() const { return head_.next_ == &head_; }

  // Return the length of the linked list. O(n).
  size_t length() const {
    size_t result = 0;
    for (Elem *e = head_.next_; e != &head_; e = e->next_) {
      result++;
    }
    return result;
  }

  // Returns first element in the list. The list must not be empty.
  T *first() const {
    ASSERT(!empty());
    return static_cast<T *>(head_.next_);
  }

  // Returns last element in the list. The list must not be empty.
  T *last() const {
    ASSERT(!empty());
    return static_cast<T *>(head_.prev_);
  }

  // Add item to the front of list.
  void prepend(T *item) { head_.append(item); }

  void append(T *item) { head_.prepend(item); }
  
  // Add item to the sorted position of list
  void insert(T *item) {
    T* head = static_cast<T *>(&head_);
    if(empty()){
      // empty list
      head->prepend(item);
      return;
    }
    T* cur = static_cast<T *>(head->next_);
    while(Comp()(item, cur) && cur!=head){
      cur = static_cast<T *>(cur->next_);
    }
    cur->prepend(item); 
  }

  bool remove(T *item) {
    // must be on the list; we don't check.
    return item->remove();
  }

  // Support for range-based iteration over a list.
  Iter begin() const { return Iter(head_.next_); }
  Iter end() const { return Iter(const_cast<Elem *>(&head_)); }

  // Iterator pointing to a given list item.
  // REQUIRES: item is a member of the list.
  Iter at(T *item) const { return Iter(item); }

 private:
  // Support for range-based iteration over a list.
  class Iter {
    friend class TSortedList;
    Elem *elem_;
    explicit Iter(Elem *elem) : elem_(elem) {}

   public:
    Iter &operator++() {
      elem_ = elem_->next_;
      return *this;
    }
    Iter &operator--() {
      elem_ = elem_->prev_;
      return *this;
    }

    bool operator!=(Iter other) const { return elem_ != other.elem_; }
    bool operator==(Iter other) const { return elem_ == other.elem_; }
    T *operator*() const { return static_cast<T *>(elem_); }
    T *operator->() const { return static_cast<T *>(elem_); }
  };
  friend class Iter;

  Elem head_;
};

}  // namespace tcmalloc

#endif  // TCMALLOC_INTERNAL_ALGORITHM_H_