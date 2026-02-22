# Compatibility shim for Ruby >= 3.2 where tainted? was removed.
# Jekyll 3.9 + Liquid 4.0.3 still calls `#tainted?` on generic objects.
# this keeps local preview working on newer Ruby without changing template data.
class Object
  unless method_defined?(:tainted?)
    def tainted?
      false
    end
  end
end
